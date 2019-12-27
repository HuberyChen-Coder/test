select  
    b.site_tp,                              --主站点
    b.sku_cate_id,                          --商品末级分类id
    max(b.sku_cate_nm) as sku_cate_nm,      --商品末级分类
    b.shpp_country_nm as country_nm,        --国家
    a.new_vc_cate_nm,                       --项目组
    if(b.sku_id regexp '[a-z_]*[0-9]+_([a-zA-Z0-9\-\.]+)',regexp_extract(b.sku_id,'[a-z_]*[0-9]+_([a-zA-Z0-9\-\.]+)',1),'no_size') as size,     --尺码
    sum(b.sale_cnt) as sale_cnt,            --销售量
    b.dt
from (
    select
        goods_sn,
        new_vc_cate_nm
    from dm.dm_gds_new_vc_cate_nm_noid_td
    where new_vc_cate_nm not in ('europe', 'bags', 'jewelry', 'accessories', 'usa',
        'make up', 'home', 'me clothing', 'me loungewear', 'me bags', 'me shoes')
) a