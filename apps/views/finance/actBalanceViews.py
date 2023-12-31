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


def actBalRegViews(request):

    return render(request, "finance/accountBalance-reg.html")

def actBalRegViews_search(request):
    actCode = request.POST.get('actCode')
    actNum = request.POST.get('actNum')
    bankCode = request.POST.get('bankCode')

    if actNum is not None and actNum != '' and bankCode is not None and bankCode != '':
        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT IFNULL(A.ACNUMBER,''), IFNULL(B.ACNUM_NAME,''), IFNULL(B.ACBKCD, ''), IFNULL(C.RESNAM,'') "
                "        ,IFNULL(A.ACDATE,''), IFNULL(A.ACAMTS, 0), IFNULL(A.ACDESC, '') "
                "       FROM ACBALANCE A "
                "       LEFT OUTER JOIN ACNUMBER B "
                "       ON A.ACNUMBER = B.ACNUMBER "
                "       LEFT OUTER JOIN OSREFCP C "
                "       ON B.ACBKCD = C.RESKEY "
                "       AND C.RECODE = 'BNK' "
                "       WHERE A.ACNUMBER LIKE '%" + actNum + "%'"
                "       AND B.ACBKCD LIKE '%" + bankCode + "%'"
                "       ORDER BY A.ACDATE"
            )
            actBalresult = cursor.fetchall()

        # 은행명 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BNK' ")
            cboBankName = cursor.fetchall()

        # 계좌번호 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER ")
            cboActNum = cursor.fetchall()

        return JsonResponse({"cboActNum": cboActNum, "cboBankName": cboBankName, "actBalList": actBalresult})


    elif actCode is not None and actCode != '' or bankCode is not None and bankCode != '':
        # 계좌명 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER, ACNUM_NAME, ACBKCD, B.RESNAM FROM ACNUMBER A "
                           "    LEFT OUTER JOIN OSREFCP B "
                           "    ON A.ACBKCD = B.RESKEY "
                           "    AND B.RECODE = 'BNK' "
                           "    WHERE ACNUMBER LIKE '%" + actCode + "%' "
                           "    AND ACBKCD LIKE '%" + bankCode + "%' ")
            actResult = cursor.fetchall()
            print(actResult)

        return JsonResponse({"actList": actResult})

    else:
        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT IFNULL(A.ACNUMBER,''), IFNULL(B.ACNUM_NAME,''), IFNULL(B.ACBKCD, ''), IFNULL(C.RESNAM,'') "
                "        ,IFNULL(A.ACDATE,''), IFNULL(A.ACAMTS, 0), IFNULL(A.ACDESC, '') "
                "       FROM ACBALANCE A "
                "       LEFT OUTER JOIN ACNUMBER B "
                "       ON A.ACNUMBER = B.ACNUMBER "
                "       LEFT OUTER JOIN OSREFCP C "
                "       ON B.ACBKCD = C.RESKEY "
                "       AND C.RECODE = 'BNK' "
                "       ORDER BY A.ACDATE"
            )
            actBalresult = cursor.fetchall()

            print(actBalresult)

        # 은행명 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BNK' ")
            inputBankType = cursor.fetchall()

        # 은행명 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BNK' ")
            cboBankName = cursor.fetchall()

        return JsonResponse({"inputBankType": inputBankType, "cboBankName": cboBankName, "actBalList": actBalresult})


def actBalRegViews_save(request):
    if 'btnSave' in request.POST:
        actNum = request.POST.get('cboActNum')
        actDate = request.POST.get('txtDate').replace('-', '')
        actAmts = request.POST.get('txtBalance')
        actDesc = request.POST.get('txtRemark')

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO ACBALANCE "
                           "   ("
                           "     ACNUMBER "
                           ",    ACDATE "
                           ",    ACAMTS "
                           ",    ACDESC "
                           ") "
                           "    VALUES "
                           "    ("
                           "    '" + actNum + "' "
                           ",   date_format(now(), '%Y%m%d') "
                           ",   '" + str(actAmts) + "' "
                           ",   '" + str(actDesc) + "' "
                           "    ) "
                           "    ON DUPLICATE  KEY "
                           "    UPDATE "
                           "     ACAMTS  = '" + str(actAmts) + "' "
                           ",    ACDESC = '" + str(actDesc) + "' "
                           )
            connection.commit()

            messages.success(request, '저장 되었습니다.')
            return render(request, 'finance/accountBalance-reg.html')

    else:
        messages.warning(request, '입력 하신 정보를 확인 해주세요.')
        return redirect('/actBalance_reg')



def actBalRegViews_dlt(request):
    if request.method == "POST":
        dataList = json.loads(request.POST.get('arrList'))
        print(dataList)
        for act in dataList:
            acc_split_list = act.split(',')
            with connection.cursor() as cursor:
                cursor.execute(" DELETE FROM ACBALANCE WHERE ACNUMBER = '" + acc_split_list[0] + "' "
                               "                        AND ACDATE = '" + acc_split_list[1] + "' ")
                connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        return render(request, 'finance/accountBalance-reg.html')