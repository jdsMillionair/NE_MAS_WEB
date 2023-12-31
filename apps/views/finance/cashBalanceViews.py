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


def cashBalRegViews(request):

    return render(request, "finance/cash-reg.html")

def cashBalRegBankViews(request):
    with connection.cursor() as cursor:
        cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BNK' ")
        banks = cursor.fetchall()

        return JsonResponse({"bankList": banks})

def cashBalRegSearchViews(request):
    # form = CustBalRegForm(request.POST or None)
    SearchBank = request.POST.get('bankCode')

    # 은행명 선택 시 조회
    if SearchBank != '' and SearchBank is not None:
        # 은행 계좌 잔액 등록 - 은행명 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BNK' AND RESKEY = '" + SearchBank + "' ")
            bankselected = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(
                            " SELECT "
                            "         IFNULL(C.RESKEY,'') AS RECODE"
                            "        ,IFNULL(C.RESNAM,'') AS BANKNM "
                            "        ,IFNULL(B.ACNUM_NAME,'') AS ACNUM_NAME "
                            "        ,IFNULL(A.ACNUMBER,'') AS ACNUMBER "
                            "        ,IFNULL(A.ACDATE,'') AS ACDATE "
                            "        ,IFNULL(A.ACAMTS, 0) AS ACAMTS "
                            "        ,IFNULL(A.ACDESC, '') AS ACDESC "
                            " FROM ACCASHP A "
                            " LEFT OUTER JOIN ACNUMBER B "
                            " ON A.ACNUMBER = B.ACNUMBER "
                            " LEFT OUTER JOIN OSREFCP C "
                            " ON B.ACBKCD = C.RESKEY "
                            " WHERE C.RECODE = 'BNK' "
                            " ORDER BY A.ACDATE "
                            " AND C.RESKEY = '" + SearchBank + "'")
            acResult = cursor.fetchall()

        return JsonResponse({'acList': acResult, "bankCombo2": bankselected})

    elif SearchBank is None or SearchBank == '':
        # 은행 계좌 잔액 등록 - 은행명 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BNK' ")
            bankresult = cursor.fetchall()

        # 은행 계좌 잔액 테이블
        with connection.cursor() as cursor:
            cursor.execute(
                           " SELECT "
                           "         IFNULL(C.RESKEY,'') AS RECODE"
                           "        ,IFNULL(C.RESNAM,'') AS BANKNM "
                           "        ,IFNULL(B.ACNUM_NAME,'') AS ACNUM_NAME "
                           "        ,IFNULL(A.ACNUMBER,'') AS ACNUMBER "
                           "        ,IFNULL(A.ACDATE,'') AS ACDATE "
                           "        ,IFNULL(A.ACAMTS, 0) AS ACAMTS "
                           "        ,IFNULL(A.ACDESC, '') AS ACDESC "
                           " FROM ACCASHP A "
                           " LEFT OUTER JOIN ACNUMBER B "
                           " ON A.ACNUMBER = B.ACNUMBER "
                           " LEFT OUTER JOIN OSREFCP C "
                           " ON B.ACBKCD = C.RESKEY "
                           " WHERE C.RECODE = 'BNK' "
                           " ORDER BY A.ACDATE "
                )
            allAcResult = cursor.fetchall()

        return JsonResponse({"bankCombo": bankresult, "acList": allAcResult})
    else:
        return redirect('/cashBalance_reg')




def cashBalRegSearchScndViews(request):
    SearchBank = request.POST.get('bankCode')

    # 은행명 선택 시 조회
    with connection.cursor() as cursor:
        cursor.execute(
            " SELECT "
            "         IFNULL(C.RESKEY,'') AS RECODE"
            "        ,IFNULL(C.RESNAM,'') AS BANKNM "
            "        ,IFNULL(B.ACNUM_NAME,'') AS ACNUM_NAME "
            "        ,IFNULL(A.ACNUMBER,'') AS ACNUMBER "
            "        ,IFNULL(A.ACDATE,'') AS ACDATE "
            "        ,IFNULL(A.ACAMTS, 0) AS ACAMTS "
            "        ,IFNULL(A.ACDESC, '') AS ACDESC "
            " FROM ACCASHP A "
            " LEFT OUTER JOIN ACNUMBER B "
            " ON A.ACNUMBER = B.ACNUMBER "
            " LEFT OUTER JOIN OSREFCP C "
            " ON B.ACBKCD = C.RESKEY "
            " WHERE C.RECODE = 'BNK' "
            " AND C.RESKEY = '" + SearchBank + "'"
            " ORDER BY A.ACDATE "

            )
        acResult = cursor.fetchall()

    return JsonResponse({'acListScnd': acResult})


def cashBalRegCboSearchViews(request):
    SearchBank = request.POST.get('bankCode')

    # 은행명 선택 시 계좌번호 란에 콤보박스에 바인딩
    with connection.cursor() as cursor:
        cursor.execute(
            " SELECT"
            "         IFNULL(C.RESKEY,'') AS RESKEY"
            "        ,IFNULL(B.ACNUM_NAME,'') AS ACNUM_NAME"
            "        ,IFNULL(A.ACNUMBER,'') AS ACNUMBER"
            " FROM ACCASHP A"
            " LEFT OUTER JOIN ACNUMBER B"
            " ON A.ACNUMBER = B.ACNUMBER"
            " LEFT OUTER JOIN OSREFCP C"
            " ON B.ACBKCD = C.RESKEY"
            " WHERE C.RECODE = 'BNK'"
            " AND C.RESKEY = '" + SearchBank + "'"
            " GROUP BY C.RESKEY, B.ACNUM_NAME, A.ACNUMBER"


            )
        acnumlist = cursor.fetchall()

    return JsonResponse({'acnumlist': acnumlist})

def cashBalRegAcNmSearchViews(request):
    SearchBankAcNum = request.POST.get('acnumcode')

    # 은행명 선택 시 계좌번호 란에 콤보박스에 바인딩
    with connection.cursor() as cursor:
        cursor.execute(
            " SELECT ACNUM_NAME FROM ACNUMBER WHERE ACNUMBER = '" + SearchBankAcNum + "'"
            )
        acnamelist = cursor.fetchall()

    return JsonResponse({'acnamelist': acnamelist})



def cashBalRegSaveViews(request):
    ActNum = request.POST.get("cboActNum")
    RAcNum = ActNum[2:]
    RegDate = request.POST.get("txtRegDate")
    RRegDate = RegDate.replace("-", "")
    Amount = request.POST.get("txtAmount")
    Bigo = request.POST.get("txtBigo")

    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO ACCASHP "
                       "   ("
                       "     ACNUMBER "
                       ",    ACDATE "
                       ",    ACAMTS "
                       ",    ACDESC "
                       ") "
                       "    VALUES "
                       "    ("
                       "    '" + str(RAcNum) + "' "
                       ",   '" + str(RRegDate) + "' "
                       ",   '" + str(Amount) + "'"
                       ",   '" + str(Bigo) + "'"
                       "    ) "
                       "    ON DUPLICATE KEY "
                       "    UPDATE "
                       "     ACAMTS = '" + str(Amount) + "' "
                       ",    ACDESC = '" + str(Bigo) + "' "
                       )
        connection.commit()
    messages.success(request, '저장 되었습니다.')
    return redirect('/cashBalance_reg')


