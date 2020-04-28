from collections import defaultdict

from django.db.models import Count
from django.utils import timezone

from drp.programs.utils import get_active_campaigns
from drp.rewards.models import AccumulationRule, Point


def process_order(order):
    campaigns = get_active_campaigns(order.business.campaigns)
    accumulation_rules = AccumulationRule.objects.filter(campaign__in=campaigns)

    # Store accumulation rules by categories and items.
    categories = defaultdict(list)
    items = defaultdict(list)
    for rule in accumulation_rules:
        if rule.category:
            categories[rule.category].append((rule.campaign, rule.value))
        if rule.item:
            items[rule.item].append((rule.campaign, rule.value))

    # Award points.
    points = []
    now = timezone.now()
    for line_item in order.line_items.all():
        category_rules = categories.get(line_item.menu_item.category, [])
        item_rules = items.get(line_item.menu_item, [])
        for campaign, points_per_item in category_rules + item_rules:
            number_of_points = points_per_item * line_item.quantity
            for i in range(number_of_points):
                expiry = (
                    None
                    if campaign.points_expire_after is None
                    else now + campaign.points_expire_after
                )
                points.append(
                    Point(
                        user=order.customer,
                        line_item=line_item,
                        currency=campaign.currency,
                        expires_at=expiry,
                    )
                )
    Point.objects.bulk_create(points)


def get_points_for_user(user, business):
    now = timezone.now()
    points_by_currency = (
        Point.objects.filter(user=user)
        .filter(redemption__isnull=True)
        .filter(currency__business=business)
        .exclude(expires_at__lt=timezone.now())
        .values("currency")
        .order_by("currency")
        .annotate(count=Count("currency"))
    )
    return {points["currency"]: points["count"] for points in points_by_currency}
