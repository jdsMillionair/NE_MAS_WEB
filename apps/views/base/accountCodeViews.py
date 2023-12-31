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

def accountCodeViews(request):

    return render(request, "base/base-accountCode.html")

def accountCodeViews_search(request):
    mainCode = request.POST.get('mainCode')
    mainCode2 = request.POST.get('mainCode2')
    codeType = request.POST.get('cboCodeType')
    codeType2 = request.POST.get('cboCodeType2')

    if mainCode != '' and mainCode is not None:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.MCODE, ''), IFNULL(A.MCODENM, ''), IFNULL(A.MDESC, ''), IFNULL(A.MSEQ, '')"
                           "    , IFNULL(A.GBN, ''), IFNULL(B.RESNAM, ''), IFNULL(A.GBN2, ''), IFNULL(C.RESNAM, '') FROM OSCODEM A "
                           "    LEFT OUTER JOIN OSREFCP B "
                           "    ON A.GBN = B.RESKEY "
                           "    AND B.RECODE = 'CGB' "
                           "    LEFT OUTER JOIN OSREFCP C "
                           "    ON A.GBN2 = C.RESKEY "
                           "    AND C.RECODE = 'AGB' "
                           "    WHERE MCODE = '" + mainCode + "' ")
            mresult = cursor.fetchall()

        return JsonResponse({"subMList": mresult})

    elif mainCode2 != '' and mainCode2 is not None:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.ACODE, ''), IFNULL(A.ACODENM, ''), IFNULL(A.ADESC, ''), IFNULL(A.ASEQ, '')"
                           "    , IFNULL(A.GBN, ''), IFNULL(B.RESNAM, ''), IFNULL(A.GBN2, ''), IFNULL(C.RESNAM, '') FROM OSCODEA A "
                           "    LEFT OUTER JOIN OSREFCP B "
                           "    ON A.GBN = B.RESKEY "
                           "    AND B.RECODE = 'CGB' "
                           "    LEFT OUTER JOIN OSREFCP C "
                           "    ON A.GBN2 = C.RESKEY "
                           "    AND C.RECODE = 'AGB' "
                           "    WHERE ACODE = '" + mainCode2 + "' ")
            aresult = cursor.fetchall()

        return JsonResponse({'subAList': aresult})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.MCODE, ''), IFNULL(A.MCODENM, ''), IFNULL(A.MSEQ, ''), IFNULL(A.MDESC, '')"
                           "    , IFNULL(A.GBN, ''), IFNULL(B.RESNAM, ''), IFNULL(A.GBN2, ''), IFNULL(C.RESNAM, '') FROM OSCODEM A "
                           "    LEFT OUTER JOIN OSREFCP B "
                           "    ON A.GBN = B.RESKEY "
                           "    AND B.RECODE = 'CGB' "
                           "    LEFT OUTER JOIN OSREFCP C "
                           "    ON A.GBN2 = C.RESKEY "
                           "    AND C.RECODE = 'AGB' "
                           "    WHERE MCODE LIKE '" + str(codeType) + "%' ORDER BY MCODE ")
            mresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.ACODE, ''), IFNULL(A.ACODENM, ''), IFNULL(A.ASEQ, ''), IFNULL(A.ADESC, '')"
                           "    , IFNULL(A.GBN, ''), IFNULL(B.RESNAM, ''), IFNULL(A.GBN2, ''), IFNULL(C.RESNAM, '') FROM OSCODEA A "
                           "    LEFT OUTER JOIN OSREFCP B "
                           "    ON A.GBN = B.RESKEY "
                           "    AND B.RECODE = 'CGB' "
                           "    LEFT OUTER JOIN OSREFCP C "
                           "    ON A.GBN2 = C.RESKEY "
                           "    AND C.RECODE = 'AGB' "
                           "    WHERE ACODE LIKE '" + str(codeType2) + "%' ORDER BY ACODE ")
            aresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'CGB' ")
            gbnesult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'AGB' ")
            gbn2result = cursor.fetchall()

        return JsonResponse({"mList": mresult, 'aList': aresult, 'cboGbn': gbnesult, 'cboGbn2': gbn2result})

def accountCodeViews_saveM(request):
    codeType = request.POST.get("cboCodeType")
    mCode = request.POST.get("txtCode_M")
    mCodeNme = request.POST.get("txtCodeNme_M")
    mSeq = request.POST.get("txtSeq_M")
    mDesc = request.POST.get("txtDesc_M")
    gbn = request.POST.get("cboGbn_M")
    gbn2 = request.POST.get("cboGbn2_M")
    # 수익4/ 비용5


    if mSeq == '' or mSeq is None:
        # with connection.cursor() as cursor:
        #     cursor.execute(" SELECT IFNULL(MAX(MCODE), 0) FROM OSCODEM WHERE MCODE LIKE '" + codeType + "%'")
        #     subresult = cursor.fetchall()
        #     x = int(subresult[0][0])
        #     x = str(x)
        #     if codeType == str(x[0]):
        #         subCode = int(x) + 1
        #     else:
        #         subCode = int(codeType + str(x).zfill(5)) + 1
        #         print(subCode)

        with connection.cursor() as cursor:
              cursor.execute(" INSERT INTO OSCODEM "
                             "   (    "
                             "     MCODE "
                             ",    MSEQ "
                             ",    MCODENM "
                             ",    MDESC "
                             ",    GBN "
                             ",    GBN2 "
                             "    ) "
                             "    VALUES "
                             "    (   "
                             "    '" + str(mCode) + "'"
                             ",   (SELECT IFNULL(MAX(A.MSEQ) + 1, 1) AS COUNTED FROM OSCODEM A)"
                             ",   '" + str(mCodeNme) + "'"
                             ",   '" + str(mDesc) + "'"
                             ",   '" + str(gbn) + "'"
                             ",   '" + str(gbn2) + "'"
                             "    )   "
                             )
              connection.commit()

              return JsonResponse({'sucYn': "Y"})

    elif mSeq:
        with connection.cursor() as cursor:
            cursor.execute("    UPDATE OSCODEM SET"
                           "     MCODENM = '" + str(mCodeNme) + "' "
                           ",    MDESC = '" + str(mDesc) + "' "
                           ",    GBN = '" + str(gbn) + "' "
                           ",    GBN2 = '" + str(gbn2) + "' "
                           "     WHERE MCODE = '" + str(mCode) + "' "
                           "     AND MSEQ = '" + str(mSeq) + "' "
                           )
            connection.commit()

            return JsonResponse({'sucYn': "Y"})

    return render(request, 'base/base-accountCode.html')


def accountCodeViews_saveA(request):
    codeType2 = request.POST.get("cboCodeType2")
    aCode = request.POST.get("txtCode_A")
    aCodeNme = request.POST.get("txtCodeNme_A")
    aSeq = request.POST.get("txtSeq_A")
    gbn = request.POST.get("cboGbn_A")
    gbn2 = request.POST.get("cboGbn2_A")

    if aSeq is None or aSeq == '':
        # with connection.cursor() as cursor:
        #     cursor.execute(" SELECT IFNULL(MAX(ACODE), 0) + 1 FROM OSCODEA WHERE ACODE LIKE '" + codeType2 + "%' ")
        #     subresult = cursor.fetchall()
        #     x = int(subresult[0][0])
        #     x = str(x)
        #     if codeType2 == str(x[0]):
        #         x = int(x)
        #         subCode = x + 1
        #     else:
        #         subCode = int(codeType2 + str(x).zfill(5)) + 1
        #         print(subCode)

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO OSCODEA "
                           "   (    "
                           "     ACODE "
                           ",    ASEQ "
                           ",    ACODENM "
                           ",    ADESC "
                           ",    GBN "
                           ",    GBN2 "
                           "    ) "
                           "    VALUES "
                           "    (   "
                           "    '" + str(aCode) + "'"
                           ",   (SELECT IFNULL (MAX(A.ASEQ) + 1,1) AS COUNTED FROM OSCODEA A)"
                           ",   '" + str(aCodeNme) + "'"
                           ",   '" + str(aDesc) + "'"
                           ",   '" + str(gbn) + "'"
                           ",   '" + str(gbn2) + "'"
                           "    )   "
                           )
            connection.commit()

            return JsonResponse({'sucYn': "Y"})

    elif aSeq:
        with connection.cursor() as cursor:
            cursor.execute("    UPDATE  OSCODEA SET"
                           "     ACODENM = '" + str(aCodeNme) + "' "
                           ",    ADESC = '" + str(aDesc) + "' "
                           ",    GBN = '" + str(gbn) + "' "
                           ",    GBN2 = '" + str(gbn2) + "' "
                           "     WHERE ACODE = '" + str(aCode) + "' "
                           "     AND ASEQ = '" + str(aSeq) + "' "
                           )
            connection.commit()

            return JsonResponse({'sucYn': "Y"})

    return render(request, 'base/base-accountCode.html')


def accountCodeViews_dltM(request):
    if request.method == "POST":
        dataList = json.loads(request.POST.get('arrList'))
        print(dataList)
        for code in dataList:
            acc_split_list = code.split(',')
            with connection.cursor() as cursor:
                cursor.execute(" DELETE FROM OSCODEM WHERE MCODE = '" + acc_split_list[0] + "'"
                               "                       AND MSEQ = '" + acc_split_list[1] + "' ")
                connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        return render(request, 'base/base-accountCode.html')

def accountCodeViews_dltA(request):
    if request.method == "POST":
        dataList = json.loads(request.POST.get('arrList'))
        print(dataList)
        for code in dataList:
            acc_split_list = code.split(',')
            with connection.cursor() as cursor:
                cursor.execute(" DELETE FROM OSCODEA WHERE ACODE = '" + acc_split_list[0] + "'"
                               "                         AND ASEQ = '" + acc_split_list[1] + "' ")
                connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        return render(request, 'base/base-accountCode.html')