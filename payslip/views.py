from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Payslip

# Create your views here.
class PayslipDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        payslips = Payslip.objects.filter(user=request.user).order_by("-id")

        latest = payslips.first()

        if not latest:
            return Response({
                "summary": [],
                "payslips":[],
                "deductions": []
            })
        
        summary = [
            {
                "label":"Net Salary",
                "value": latest.net_salary,
            },
            {
                "label":"Basic Salary",
                "value": latest.basic_salary,
            },
            {
                "label":"Total Earnings",
                "value": latest.total_earnings,
            },
            {
                "label":"Total Deductions",
                "value": latest.total_deductions,
            },
            {
                "label":"Current Month",
                "value": latest.month,
            },
        ]

        payslip_data = []

        for p in payslips:
            payslip_data.append({
                "id":p.id,
                "month":p.month,
                "net":p.net_salary,
                "status":p.status,
            })

        deductions = [
            {"label":"Tax","amount":latest.tax},
            {"label":"PF","amount":latest.pf},
            {"label":"Insurance","amount":latest.insurance},
            {"label":"Performance Bonus","amount":latest.bonus},
            {"label":"Other Allowances","amount":latest.allowance},
        ]

        return Response({
            "summary":summary,
            "payslips":payslip_data,
            "deductions":deductions
        })
