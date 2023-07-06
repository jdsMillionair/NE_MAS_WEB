import json
from django.shortcuts import render, redirect
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.db import connection

# 매입
def purTransSearchViews(request):

    return render(request, "finance/purchases-trans-report.html")

# 매출
def saleTransSearchViews(request):

    return render(request, "finance/sales-trans-report.html")


def purTransSearchViews_search(request):
    Year = request.POST.get('Year')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT ITEM, UP_CODE, CUST_NME, GUBUN, DANGA "
                       "     , SUM(M01) AS M01, sum(M01_S) AS M01_S, SUM(M01_A) AS M01_A "
                       "     , SUM(M02) AS M02, sum(M02_S) AS M02_S, SUM(M02_A) AS M02_A "
                       "     , SUM(M03) AS M03, sum(M03_S) AS M03_S, SUM(M03_A) AS M03_A "
                       "     , SUM(M04) AS M04, sum(M04_S) AS M04_S, SUM(M04_A) AS M04_A "
                       "     , SUM(M05) AS M05, sum(M05_S) AS M05_S, SUM(M05_A) AS M05_A "
                       "     , SUM(M06) AS M06, sum(M06_S) AS M06_S, SUM(M06_A) AS M06_A "
                       "     , SUM(M07) AS M07, sum(M07_S) AS M07_S, SUM(M07_A) AS M07_A "
                       "     , SUM(M08) AS M08, sum(M08_S) AS M08_S, SUM(M08_A) AS M08_A "
                       "     , SUM(M09) AS M09, sum(M09_S) AS M09_S, SUM(M09_A) AS M09_A "
                       "     , SUM(M10) AS M10, sum(M10_S) AS M10_S, SUM(M10_A) AS M10_A "
                       "     , SUM(M11) AS M11, sum(M11_S) AS M11_S, SUM(M11_A) AS M11_A "
                       "     , SUM(M12) AS M12, sum(M12_S) AS M12_S, SUM(M12_A) AS M12_A "
                       "     FROM ( "
                       "     SELECT C.ITEM, UP_CODE, C.CUST_NME, C.GUBUN, C.DANGA "
                       "          , ifnull(C.MONTH01, 0) AS M01 "
                       "          , ifnull(C.MONTH01_S, 0) AS M01_S "
                       "          , ifnull(C.MONTH01_A, 0) AS M01_A "
                       "          , ifnull(C.MONTH02, 0) AS M02 "
                       "          , ifnull(C.MONTH02_S, 0) AS M02_S "
                       "          , ifnull(C.MONTH02_A, 0) AS M02_A "
                       "          , ifnull(C.MONTH03, 0) AS M03 "
                       "          , ifnull(C.MONTH03_S, 0) AS M03_S "
                       "          , ifnull(C.MONTH03_A, 0) AS M03_A "
                       "          , ifnull(C.MONTH04, 0) AS M04 "
                       "          , ifnull(C.MONTH04_S, 0) AS M04_S "
                       "          , ifnull(C.MONTH04_A, 0) AS M04_A "
                       "          , ifnull(C.MONTH05, 0) AS M05 "
                       "          , ifnull(C.MONTH05_S, 0) AS M05_S "
                       "          , ifnull(C.MONTH05_A, 0) AS M05_A "
                       "          , ifnull(C.MONTH06, 0) AS M06 "
                       "          , ifnull(C.MONTH06_S, 0) AS M06_S "
                       "          , ifnull(C.MONTH06_A, 0) AS M06_A "
                       "          , ifnull(C.MONTH07, 0) AS M07 "
                       "          , ifnull(C.MONTH07_S, 0) AS M07_S "
                       "          , ifnull(C.MONTH07_A, 0) AS M07_A "
                       "          , ifnull(C.MONTH08, 0) AS M08 "
                       "          , ifnull(C.MONTH08_S, 0) AS M08_S "
                       "          , ifnull(C.MONTH08_A, 0) AS M08_A "
                       "          , ifnull(C.MONTH09, 0) AS M09 "
                       "          , ifnull(C.MONTH09_S, 0) AS M09_S "
                       "          , ifnull(C.MONTH09_A, 0) AS M09_A "
                       "          , ifnull(C.MONTH10, 0) AS M10 "
                       "          , ifnull(C.MONTH10_S, 0) AS M10_S "
                       "          , ifnull(C.MONTH10_A, 0) AS M10_A "
                       "          , ifnull(C.MONTH11, 0) AS M11 "
                       "          , ifnull(C.MONTH11_S, 0) AS M11_S "
                       "          , ifnull(C.MONTH11_A, 0) AS M11_A "
                       "          , ifnull(C.MONTH12, 0) AS M12 "
                       "          , ifnull(C.MONTH12_S, 0) AS M12_S "
                       "          , ifnull(C.MONTH12_A, 0) AS M12_A "
                       "     FROM (SELECT A.ITEM                                                                                AS ITEM "
                       "                , A.UP_CODE                                                                             AS UP_CODE "
                       "                , B.CUST_NME                                                                            AS CUST_NME "
                       "                , A.GUBUN                                                                               AS GUBUN "
                       "                , A.DANGA                                                                               AS DANGA "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '01') THEN SUM(A.QTY) END)    AS MONTH01 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '01') THEN SUM(A.SUPPLY) END) AS MONTH01_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '01') THEN SUM(A.AMTS) END)   AS MONTH01_A "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '02') THEN SUM(A.QTY) END)    AS MONTH02 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '02') THEN SUM(A.SUPPLY) END) AS MONTH02_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '02') THEN SUM(A.AMTS) END)   AS MONTH02_A "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '03') THEN SUM(A.QTY) END)    AS MONTH03 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '03') THEN SUM(A.SUPPLY) END) AS MONTH03_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '03') THEN SUM(A.AMTS) END)   AS MONTH03_A "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '04') THEN SUM(A.QTY) END)    AS MONTH04 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '04') THEN SUM(A.SUPPLY) END) AS MONTH04_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '04') THEN SUM(A.AMTS) END)   AS MONTH04_A "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '05') THEN SUM(A.QTY) END)    AS MONTH05 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '05') THEN SUM(A.SUPPLY) END) AS MONTH05_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '05') THEN SUM(A.AMTS) END)   AS MONTH05_A "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '06') THEN SUM(A.QTY) END)    AS MONTH06 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '06') THEN SUM(A.SUPPLY) END) AS MONTH06_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '06') THEN SUM(A.AMTS) END)   AS MONTH06_A "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '07') THEN SUM(A.QTY) END)    AS MONTH07 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '07') THEN SUM(A.SUPPLY) END) AS MONTH07_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '07') THEN SUM(A.AMTS) END)   AS MONTH07_A "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '08') THEN SUM(A.QTY) END)    AS MONTH08 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '08') THEN SUM(A.SUPPLY) END) AS MONTH08_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '08') THEN SUM(A.AMTS) END)   AS MONTH08_A "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '09') THEN SUM(A.QTY) END)    AS MONTH09 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '09') THEN SUM(A.SUPPLY) END) AS MONTH09_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '09') THEN SUM(A.AMTS) END)   AS MONTH09_A "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '10') THEN SUM(A.QTY) END)    AS MONTH10 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '10') THEN SUM(A.SUPPLY) END) AS MONTH10_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '10') THEN SUM(A.AMTS) END)   AS MONTH10_A "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '11') THEN SUM(A.QTY) END)    AS MONTH11 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '11') THEN SUM(A.SUPPLY) END) AS MONTH11_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '11') THEN SUM(A.AMTS) END)   AS MONTH11_A "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '12') THEN SUM(A.QTY) END)    AS MONTH12 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '12') THEN SUM(A.SUPPLY) END) AS MONTH12_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '12') THEN SUM(A.AMTS) END)   AS MONTH12_A "
                       "           FROM OSBILL A "
                       "           LEFT OUTER JOIN MIS1TB003 B "
                       "           ON A.UP_CODE = B.CUST_NBR "
                       "           WHERE GUBUN = '1' "
                       "           AND YEAR(BAL_DD) = '" + Year + "' "
                       "           GROUP BY A.ITEM, A.UP_CODE, A.DANGA, A.GUBUN, DATE_FORMAT(BAL_DD, '%Y%m')) C "
                       "   ) BB "
                       " GROUP BY ITEM, UP_CODE, CUST_NME, GUBUN, DANGA ")

        mainresult = cursor.fetchall()

    return JsonResponse({"mainList": mainresult})

def saleTransSearchViews_search(request):
    Year = request.POST.get('Year')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT ITEM, UP_CODE, CUST_NME, GUBUN, DANGA "
                       "     ,SUM(M01) AS M01, sum(M01_S) AS M01_S ,SUM(M01_A) AS M01_A "
                       "     ,SUM(M02), sum(M02_S),SUM(M02_A) "
                       "     ,SUM(M03), sum(M03_S),SUM(M03_A) "
                       "     ,SUM(M04), sum(M04_S),SUM(M04_A) "
                       "     ,SUM(M05), sum(M05_S),SUM(M05_A) "
                       "     ,SUM(M06), sum(M06_S),SUM(M06_A) "
                       "     ,SUM(M07), sum(M07_S),SUM(M07_A) "
                       "     ,SUM(M08), sum(M08_S),SUM(M08_A) "
                       "     ,SUM(M09), sum(M09_S),SUM(M09_A) "
                       "     ,SUM(M10), sum(M10_S),SUM(M10_A) "
                       "     ,SUM(M11), sum(M11_S),SUM(M11_A) "
                       "     ,SUM(M12), sum(M12_S),SUM(M12_A) "
                       "     FROM ( "
                       "     SELECT C.ITEM, UP_CODE, C.CUST_NME, C.GUBUN, C.DANGA "
                       "          , ifnull(C.MONTH01, 0) AS M01 "
                       "          , ifnull(C.MONTH01_S, 0) AS M01_S "
                       "          , ifnull(C.MONTH01_A, 0) AS M01_A "
                       "          , ifnull(C.MONTH02, 0) AS M02 "
                       "          , ifnull(C.MONTH02_S, 0) AS M02_S "
                       "          , ifnull(C.MONTH02_A, 0) AS M02_A "
                       "          , ifnull(C.MONTH03, 0) AS M03 "
                       "          , ifnull(C.MONTH03_S, 0) AS M03_S "
                       "          , ifnull(C.MONTH03_A, 0) AS M03_A "
                       "          , ifnull(C.MONTH04, 0) AS M04 "
                       "          , ifnull(C.MONTH04_S, 0) AS M04_S "
                       "          , ifnull(C.MONTH04_A, 0) AS M04_A "
                       "          , ifnull(C.MONTH05, 0) AS M05 "
                       "          , ifnull(C.MONTH05_S, 0) AS M05_S "
                       "          , ifnull(C.MONTH05_A, 0) AS M05_A "
                       "          , ifnull(C.MONTH06, 0) AS M06 "
                       "          , ifnull(C.MONTH06_S, 0) AS M06_S "
                       "          , ifnull(C.MONTH06_A, 0) AS M06_A "
                       "          , ifnull(C.MONTH07, 0) AS M07 "
                       "          , ifnull(C.MONTH07_S, 0) AS M07_S "
                       "          , ifnull(C.MONTH07_A, 0) AS M07_A "
                       "          , ifnull(C.MONTH08, 0) AS M08 "
                       "          , ifnull(C.MONTH08_S, 0) AS M08_S "
                       "          , ifnull(C.MONTH08_A, 0) AS M08_A "
                       "          , ifnull(C.MONTH09, 0) AS M09 "
                       "          , ifnull(C.MONTH09_S, 0) AS M09_S "
                       "          , ifnull(C.MONTH09_A, 0) AS M09_A "
                       "          , ifnull(C.MONTH10, 0) AS M10 "
                       "          , ifnull(C.MONTH10_S, 0) AS M10_S "
                       "          , ifnull(C.MONTH10_A, 0) AS M10_A "
                       "          , ifnull(C.MONTH11, 0) AS M11 "
                       "          , ifnull(C.MONTH11_S, 0) AS M11_S "
                       "          , ifnull(C.MONTH11_A, 0) AS M11_A "
                       "          , ifnull(C.MONTH12, 0) AS M12 "
                       "          , ifnull(C.MONTH12_S, 0) AS M12_S "
                       "          , ifnull(C.MONTH12_A, 0) AS M12_A "
                       "     FROM (SELECT A.ITEM                                                                                AS ITEM "
                       "                , A.UP_CODE                                                                             AS UP_CODE "
                       "                , B.CUST_NME                                                                            AS CUST_NME "
                       "                , A.GUBUN                                                                               AS GUBUN "
                       "                , A.DANGA                                                                               AS DANGA "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '01') THEN SUM(A.QTY) END)    AS MONTH01 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '01') THEN SUM(A.SUPPLY) END) AS MONTH01_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '01') THEN SUM(A.AMTS) END)   AS MONTH01_A "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '02') THEN SUM(A.QTY) END)    AS MONTH02 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '02') THEN SUM(A.SUPPLY) END) AS MONTH02_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '02') THEN SUM(A.AMTS) END)   AS MONTH02_A "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '03') THEN SUM(A.QTY) END)    AS MONTH03 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '03') THEN SUM(A.SUPPLY) END) AS MONTH03_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '03') THEN SUM(A.AMTS) END)   AS MONTH03_A "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '04') THEN SUM(A.QTY) END)    AS MONTH04 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '04') THEN SUM(A.SUPPLY) END) AS MONTH04_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '04') THEN SUM(A.AMTS) END)   AS MONTH04_A "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '05') THEN SUM(A.QTY) END)    AS MONTH05 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '05') THEN SUM(A.SUPPLY) END) AS MONTH05_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '05') THEN SUM(A.AMTS) END)   AS MONTH05_A "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '06') THEN SUM(A.QTY) END)    AS MONTH06 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '06') THEN SUM(A.SUPPLY) END) AS MONTH06_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '06') THEN SUM(A.AMTS) END)   AS MONTH06_A "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '07') THEN SUM(A.QTY) END)    AS MONTH07 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '07') THEN SUM(A.SUPPLY) END) AS MONTH07_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '07') THEN SUM(A.AMTS) END)   AS MONTH07_A "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '08') THEN SUM(A.QTY) END)    AS MONTH08 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '08') THEN SUM(A.SUPPLY) END) AS MONTH08_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '08') THEN SUM(A.AMTS) END)   AS MONTH08_A "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '09') THEN SUM(A.QTY) END)    AS MONTH09 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '09') THEN SUM(A.SUPPLY) END) AS MONTH09_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '09') THEN SUM(A.AMTS) END)   AS MONTH09_A "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '10') THEN SUM(A.QTY) END)    AS MONTH10 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '10') THEN SUM(A.SUPPLY) END) AS MONTH10_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '10') THEN SUM(A.AMTS) END)   AS MONTH10_A "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '11') THEN SUM(A.QTY) END)    AS MONTH11 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '11') THEN SUM(A.SUPPLY) END) AS MONTH11_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '11') THEN SUM(A.AMTS) END)   AS MONTH11_A "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '12') THEN SUM(A.QTY) END)    AS MONTH12 "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '12') THEN SUM(A.SUPPLY) END) AS MONTH12_S "
                       "                , (CASE WHEN DATE_FORMAT(BAL_DD, '%Y%m') = CONCAT('2023', '12') THEN SUM(A.AMTS) END)   AS MONTH12_A "
                       "           FROM OSBILL A "
                       "           LEFT OUTER JOIN MIS1TB003 B "
                       "           ON A.UP_CODE = B.CUST_NBR "
                       "           WHERE GUBUN = '2' "
                       "           AND YEAR(BAL_DD) = '" + Year + "' "
                       "           GROUP BY A.ITEM, A.UP_CODE, A.DANGA, A.GUBUN, DATE_FORMAT(BAL_DD, '%Y%m')) C "
                       "   ) BB "
                       " GROUP BY ITEM, UP_CODE, CUST_NME, GUBUN, DANGA ")

        mainresult = cursor.fetchall()

    return JsonResponse({"mainList": mainresult})


def custLedgerViews(request):

    return render(request, "finance/custledger-report.html")

def custLedgerViews_search(request):
    Year = request.POST.get('Year')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(A.ITEM, ''), IFNULL(A.UP_CODE, ''), IFNULL(B.CUST_NME, '')"
                       "    , IFNULL(A.GUBUN, ''), IFNULL(A.DANGA, ''), IFNULL(SUM(A.QTY), 0)"
                       "    , IFNULL(SUM(A.SUPPLY), 0), IFNULL(SUM(A.AMTS), 0), IFNULL(DATE_FORMAT(BAL_DD, '%Y%m'), '')"
                       "    , IFNULL(SUM(ACAMTS), 0), IFNULL(ACIOGB, '') "
                       "    FROM OSBILL A  "
                       "    LEFT OUTER JOIN MIS1TB003 B "
                       "    ON A.UP_CODE = B.CUST_NBR "
                       "    WHERE GUBUN = '2' "
                       "    AND YEAR(BAL_DD) = '" + Year + "' "
                       "    GROUP BY A.ITEM, A.UP_CODE, A.DANGA, A.GUBUN, DATE_FORMAT(BAL_DD, '%Y%m') "
                       "    ORDER BY A.ITEM, A.UP_CODE, A.DANGA, A.GUBUN, DATE_FORMAT(BAL_DD, '%Y%m') ")

        mainresult = cursor.fetchall()

    return JsonResponse({"mainList": mainresult})