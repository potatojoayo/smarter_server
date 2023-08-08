from cs.models import CouponMaster


def run():
    CouponMaster.objects.create(price=30000, count_per_issue=3, name="추천인쿠폰", type="추천인쿠폰", expire_day=30,
                                coupon_message="추천인쿠폰이 발급되었습니다.")
    CouponMaster.objects.create(price=10000, count_per_issue=5, name="신규가입쿠폰", type="신규가입쿠폰", expire_day=30, coupon_message="신규가입쿠폰이 발급되었습니다.")
    CouponMaster.objects.create(price=50000, count_per_issue=1, name="보안강화 이벤트 쿠폰", type="수동쿠폰", expire_day=30,
                                coupon_message="보안강화를 위한 정보 등록 보상 이벤트 쿠폰 50,000원이 지급되었습니다.")