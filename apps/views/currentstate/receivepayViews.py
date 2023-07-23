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


def receivepaySheetViews(request):

    return render(request, "currentstate/receive-pay-banksheet.html")


def receivepaySheetViews_search(request):
    cboBank = request.POST.get('cboBank')
    cboAccount = request.POST.get('cboAccount')
    strDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')

    if cboBank != '':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ACBKCD = '" + str(cboBank) + "' ")

            cboAresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM ")

            titleresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL((BALANCE - OAMTS) + IAMTS, 0) AS TOTAL FROM( "
                           "         SELECT "
                           "          IFNULL(SUM(A.ACAMTS), 0) AS BALANCE "
                           "         ,(SELECT IFNULL(SUM(A.ACAMTS), 0) AS OAMTS FROM SISACCTT A LEFT OUTER JOIN ACNUMBER B ON A.ACACNUMBER = B.ACNUMBER WHERE A.ACIOGB = '1' AND A.ACDATE < '" + strDate + "' AND B.ACBKCD = '" + str(cboBank) + "') AS OAMTS "
                           "         ,(SELECT IFNULL(SUM(A.ACAMTS), 0) AS IAMTS FROM SISACCTT A LEFT OUTER JOIN ACNUMBER B ON A.ACACNUMBER = B.ACNUMBER WHERE A.ACIOGB = '2' AND A.ACDATE < '" + strDate + "' AND B.ACBKCD = '" + str(cboBank) + "') AS IAMTS "
                           "          FROM ACBALANCE A "
                           "          LEFT OUTER JOIN ACNUMBER B ON A.ACNUMBER = B.ACNUMBER "
                           "          WHERE A.ACDATE < '" + strDate + "' AND B.ACBKCD = '" + str(cboBank) + "' "
                           " ) A ")

            totalresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(UN.ACDATE, ''), IFNULL(UN.ACIOGB, ''), IFNULL(UN.RESNAM, ''), IFNULL(UN.OACAMTS, 0), IFNULL(UN.IACAMTS, 0) "
                           "      , IFNULL(UN.ACCUST, ''), IFNULL(UN.CUST_NME, ''), IFNULL(UN.ACACNUMBER, ''), IFNULL(UN.ACNUM_NAME, ''), IFNULL(UN.MCODE, ''), IFNULL(UN.MCODENM, '') "
                           " FROM( "
                           "         SELECT IFNULL(A.ACDATE, '') AS ACDATE, IFNULL(A.ACIOGB, '') AS ACIOGB, IFNULL(B.RESNAM, '') AS RESNAM, IFNULL(A.ACAMTS, 0) AS OACAMTS, 0 AS IACAMTS "
                           "              , IFNULL(A.ACCUST, '') AS ACCUST, IFNULL(C.CUST_NME, '') AS CUST_NME "
                           "             , IFNULL(A.ACACNUMBER, '') AS ACACNUMBER, IFNULL(D.ACNUM_NAME, '') AS ACNUM_NAME, IFNULL(A.MCODE, '') AS MCODE, IFNULL(E.MCODENM, '') AS MCODENM "
                           "         FROM SISACCTT A "
                           "         LEFT OUTER JOIN OSREFCP B "
                           "         ON A.ACIOGB = B.RESKEY "
                           "         AND B.RECODE = 'OUA' "
                           "         LEFT OUTER JOIN MIS1TB003 C "
                           "         ON A.ACCUST = C.CUST_NBR "
                           "         LEFT OUTER JOIN ACNUMBER D "
                           "         ON A.ACACNUMBER = D.ACNUMBER "
                           "         LEFT OUTER JOIN OSCODEM E "
                           "         ON A.MCODE = E.MCODE "
                           "         WHERE A.ACIOGB = '1' "
                           "         UNION ALL "
                           "         SELECT IFNULL(A.ACDATE, ''), IFNULL(A.ACIOGB, ''), IFNULL(B.RESNAM, ''), 0 AS OACAMTS, IFNULL(A.ACAMTS, 0) AS IACAMTS "
                           "             , IFNULL(A.ACCUST, ''), IFNULL(C.CUST_NME, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(D.ACNUM_NAME, ''), IFNULL(A.MCODE, ''), IFNULL(E.MCODENM, '') "
                           "         FROM SISACCTT A "
                           "         LEFT OUTER JOIN OSREFCP B "
                           "         ON A.ACIOGB = B.RESKEY "
                           "         AND B.RECODE = 'OUA' "
                           "         LEFT OUTER JOIN MIS1TB003 C "
                           "         ON A.ACCUST = C.CUST_NBR "
                           "         LEFT OUTER JOIN ACNUMBER D "
                           "         ON A.ACACNUMBER = D.ACNUMBER "
                           "         LEFT OUTER JOIN OSCODEM E "
                           "         ON A.MCODE = E.MCODE "
                           "         WHERE A.ACIOGB = '2' "
                           "         ) UN "
                           " LEFT OUTER JOIN ACNUMBER CC "
                           " ON UN.ACACNUMBER = CC.ACNUMBER "
                           " WHERE UN.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' AND CC.ACBKCD = '" + str(cboBank) + "'  ORDER BY UN.ACDATE ")

            mainresult = cursor.fetchall()

        return JsonResponse({'cboAccount': cboAresult, 'titleList': titleresult, 'totalList': totalresult, 'mainList': mainresult})

    if cboAccount != '':

        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL((BALANCE - OAMTS) + IAMTS, 0) AS TOTAL FROM( "
                           "         SELECT "
                           "          IFNULL(SUM(ACAMTS), 0) AS BALANCE "
                           "         ,(SELECT IFNULL(SUM(ACAMTS), 0) AS OAMTS FROM SISACCTT WHERE ACIOGB = '1' AND ACDATE < '" + strDate + "' AND ACACNUMBER = '" + str(cboAccount) + "') AS OAMTS "
                           "         ,(SELECT IFNULL(SUM(ACAMTS), 0) AS IAMTS FROM SISACCTT WHERE ACIOGB = '2' AND ACDATE < '" + strDate + "' AND ACACNUMBER = '" + str(cboAccount) + "') AS IAMTS "
                           "          FROM ACBALANCE"
                           "          WHERE ACDATE < '" + strDate + "' AND ACNUMBER = '" + str(cboAccount) + "' "
                           " ) A ")

            totalresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(UN.ACDATE, ''), IFNULL(UN.ACIOGB, ''), IFNULL(UN.RESNAM, ''), IFNULL(UN.OACAMTS, 0), IFNULL(UN.IACAMTS, 0) "
                           "      , IFNULL(UN.ACCUST, ''), IFNULL(UN.CUST_NME, ''), IFNULL(UN.ACACNUMBER, ''), IFNULL(UN.ACNUM_NAME, ''), IFNULL(UN.MCODE, ''), IFNULL(UN.MCODENM, '') "
                           " FROM( "
                           "         SELECT IFNULL(A.ACDATE, '') AS ACDATE, IFNULL(A.ACIOGB, '') AS ACIOGB, IFNULL(B.RESNAM, '') AS RESNAM, IFNULL(A.ACAMTS, 0) AS OACAMTS, 0 AS IACAMTS "
                           "              , IFNULL(A.ACCUST, '') AS ACCUST, IFNULL(C.CUST_NME, '') AS CUST_NME "
                           "             , IFNULL(A.ACACNUMBER, '') AS ACACNUMBER, IFNULL(D.ACNUM_NAME, '') AS ACNUM_NAME, IFNULL(A.MCODE, '') AS MCODE, IFNULL(E.MCODENM, '') AS MCODENM "
                           "         FROM SISACCTT A "
                           "         LEFT OUTER JOIN OSREFCP B "
                           "         ON A.ACIOGB = B.RESKEY "
                           "         AND B.RECODE = 'OUA' "
                           "         LEFT OUTER JOIN MIS1TB003 C "
                           "         ON A.ACCUST = C.CUST_NBR "
                           "         LEFT OUTER JOIN ACNUMBER D "
                           "         ON A.ACACNUMBER = D.ACNUMBER "
                           "         LEFT OUTER JOIN OSCODEM E "
                           "         ON A.MCODE = E.MCODE "
                           "         WHERE A.ACIOGB = '1' "
                           "         UNION ALL "
                           "         SELECT IFNULL(A.ACDATE, ''), IFNULL(A.ACIOGB, ''), IFNULL(B.RESNAM, ''), 0 AS OACAMTS, IFNULL(A.ACAMTS, 0) AS IACAMTS "
                           "             , IFNULL(A.ACCUST, ''), IFNULL(C.CUST_NME, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(D.ACNUM_NAME, ''), IFNULL(A.MCODE, ''), IFNULL(E.MCODENM, '') "
                           "         FROM SISACCTT A "
                           "         LEFT OUTER JOIN OSREFCP B "
                           "         ON A.ACIOGB = B.RESKEY "
                           "         AND B.RECODE = 'OUA' "
                           "         LEFT OUTER JOIN MIS1TB003 C "
                           "         ON A.ACCUST = C.CUST_NBR "
                           "         LEFT OUTER JOIN ACNUMBER D "
                           "         ON A.ACACNUMBER = D.ACNUMBER "
                           "         LEFT OUTER JOIN OSCODEM E "
                           "         ON A.MCODE = E.MCODE "
                           "         WHERE A.ACIOGB = '2' "
                           "         ) UN "
                           " WHERE UN.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' AND UN.ACACNUMBER = '" + str(cboAccount) + "'  ORDER BY UN.ACDATE ")

            mainresult = cursor.fetchall()

        return JsonResponse({'totalList': totalresult, 'mainList': mainresult})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BNK' ")
            bankresult = cursor.fetchall()
            bank = bankresult[0][0]

            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ACBKCD = '" + bank + "' ")

            cboAresult = cursor.fetchall()

        return JsonResponse({"cboBank": bankresult, 'cboAccount': cboAresult})