import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import SubAllotmentAdvice, ProvinceAllotment, CISAllotment, ProgramOfWork, ProgramOfWorkItem
from .forms import SubAllotmentAdviceForm
from .models import AllotmentStatement
from django.db.models.functions import ExtractYear
from django.db.models import Q
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def save_province_table(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # data contains: office, province, headers, data
            # Save to your model here if needed
            print(data)  # check terminal to confirm it's receiving
            return JsonResponse({'ok': True})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)})
    return JsonResponse({'ok': False, 'error': 'Invalid method'})



def search_suggestions(request):
    term = request.GET.get('term', '')

    suggestions = []

    if term:
        records = SubAllotmentAdvice.objects.filter(
            Q(advice_number__icontains=term) |
            Q(description__icontains=term) |
            Q(region__icontains=term) |
            Q(to_location__icontains=term)
        )[:10]  

        for record in records:
            suggestions.append({
                'id': record.id,
                'advice_number': record.advice_number,
                'description': record.description,
            })

    return JsonResponse(suggestions, safe=False)


def index(request):

    q = request.GET.get('q', '')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        results = SubAllotmentAdvice.objects.filter(
            Q(advice_number__icontains=q)
        ).prefetch_related('province_allotments__cis_allotments')

        return JsonResponse({
            'results': [
                {
                    'pk': r.pk,
                    'advice_number': r.advice_number,
                    'description': r.description or '',
                    'total_amount': str(r.total_amount),
                    'cis_list': [
                        cis.cis_name
                        for prov in r.province_allotments.all()
                        for cis in prov.cis_allotments.all()
                    ],
                }
                for r in results
            ]
        })

    # rest of your normal page load code below...

    # NORMAL PAGE LOAD
    fund = request.GET.get('fund', '')
    year = request.GET.get('year', '')
    search_query = request.GET.get('search_query', '')

    advices = SubAllotmentAdvice.objects.prefetch_related(
        'province_allotments__cis_allotments'
    ).all()

    if fund:
        advices = advices.filter(advice_number__icontains=fund)

    if year:
        advices = advices.filter(advice_number__icontains=year)

    if search_query:
        advices = advices.filter(
            Q(advice_number__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(region__icontains=search_query) |
            Q(to_location__icontains=search_query)
        )

    def extract_years(fund_code):
        nums = SubAllotmentAdvice.objects.filter(
            advice_number__icontains=fund_code
        ).values_list('advice_number', flat=True)

        years = set()

        for num in nums:
            parts = num.split('-')
            for part in parts:
                if part.isdigit() and len(part) == 4:
                    years.add(int(part))

        return sorted(years)

    context = {
        'advices': advices,
        'active_fund': fund,
        'active_year': year,
        'search_query': search_query,
        'cob_years': extract_years('COB'),
        'lfps_years': extract_years('LFPs'),
        'carp_years': extract_years('CARP'),
    }

    return render(request, 'nia_app/index.html', context)

def create_advice(request):
    if request.method == 'POST':
        # Strip commas from total_amount before form validation
        post_data = request.POST.copy()
        total_str = post_data.get('total_amount', '0').replace(',', '')
        post_data['total_amount'] = total_str if total_str else '0'

        form = SubAllotmentAdviceForm(post_data)
        try:
            provinces_data = json.loads(request.POST.get('provinces_data', '[]'))
        except json.JSONDecodeError:
            provinces_data = []

        if form.is_valid():
            advice = form.save(commit=False)
            advice.amount_in_words = request.POST.get('amount_in_words', '')
            advice.save()
            for p_idx, prov in enumerate(provinces_data):
                prov_obj = ProvinceAllotment.objects.create(
                    sub_allotment=advice,
                    province_name=prov.get('name', ''),
                    province_total=prov.get('total', 0) or 0,
                    order=p_idx,
                )
                for c_idx, cis in enumerate(prov.get('cis_list', [])):
                    CISAllotment.objects.create(
                        province_allotment=prov_obj,
                        cis_name=cis.get('name', ''),
                        amount=cis.get('amount', 0) or 0,
                        order=c_idx,
                    )
            messages.success(request, f'Record "{advice.advice_number}" saved successfully!')
            return redirect('detail_advice', pk=advice.pk)

        else:
            messages.error(request, 'Please fix the errors below.')
            fund = request.GET.get('fund', '')
            return render(request, 'nia_app/form.html', {
                'form': form,
                'title': 'New Sub-Allotment Advice',
                'action': 'Create',
                'existing_provinces': request.POST.get('provinces_data', '[]'),
                'submitted': request.POST,
                'fund': fund,
            })
    else:
        form = SubAllotmentAdviceForm()

    fund = request.GET.get('fund', '')
    return render(request, 'nia_app/form.html', {
        'form': form, 'title': 'New Sub-Allotment Advice', 'action': 'Create',
        'fund': fund,
    })


def detail_advice(request, pk):
    advice = get_object_or_404(
        SubAllotmentAdvice.objects.prefetch_related('province_allotments__cis_allotments'), pk=pk)
    num = advice.advice_number.upper()
    if 'COB' in num: fund = 'COB'
    elif 'CARP' in num: fund = 'CARP'
    elif 'LFP' in num: fund = 'LFPs'
    else: fund = ''
    return render(request, 'nia_app/detail.html', {'advice': advice, 'fund': fund})


def edit_advice(request, pk):
    advice = get_object_or_404(SubAllotmentAdvice, pk=pk)
    if request.method == 'POST':
        # Strip commas from total_amount before form validation
        post_data = request.POST.copy()
        total_str = post_data.get('total_amount', '0').replace(',', '')
        post_data['total_amount'] = total_str if total_str else '0'

        form = SubAllotmentAdviceForm(post_data, instance=advice)
        try:
            provinces_data = json.loads(request.POST.get('provinces_data', '[]'))
        except json.JSONDecodeError:
            provinces_data = []

        if form.is_valid():
            advice = form.save(commit=False)
            advice.amount_in_words = request.POST.get('amount_in_words', '')
            advice.save()
            advice.province_allotments.all().delete()
            for p_idx, prov in enumerate(provinces_data):
                prov_obj = ProvinceAllotment.objects.create(
                    sub_allotment=advice,
                    province_name=prov.get('name', ''),
                    province_total=prov.get('total', 0) or 0,
                    order=p_idx,
                )
                for c_idx, cis in enumerate(prov.get('cis_list', [])):
                    CISAllotment.objects.create(
                        province_allotment=prov_obj,
                        cis_name=cis.get('name', ''),
                        amount=cis.get('amount', 0) or 0,
                        order=c_idx,
                    )
            messages.success(request, 'Record updated successfully!')
            return redirect('detail_advice', pk=advice.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = SubAllotmentAdviceForm(instance=advice)

    existing_provinces = [
        {
            'name': p.province_name,
            'total': float(p.province_total),
            'cis_list': [{'name': c.cis_name, 'amount': float(c.amount)} for c in p.cis_allotments.all()]
        }
        for p in advice.province_allotments.all()
    ]

    num = advice.advice_number.upper()
    if 'COB' in num: fund = 'COB'
    elif 'CARP' in num: fund = 'CARP'
    elif 'LFP' in num: fund = 'LFPs'
    else: fund = ''
    return render(request, 'nia_app/form.html', {
        'form': form,
        'title': f'Edit — {advice.advice_number}',
        'action': 'Update',
        'existing_provinces': json.dumps(existing_provinces),
        'advice': advice,
        'fund': fund,
    })


def delete_advice(request, pk):
    advice = get_object_or_404(SubAllotmentAdvice, pk=pk)
    if request.method == 'POST':
        num = advice.advice_number
        advice.delete()
        messages.success(request, f'Record "{num}" deleted.')
        return redirect('index')
    return render(request, 'nia_app/confirm_delete.html', {'advice': advice})


# ─── Allotment Statement Views ────────────────────────────────────────────────
from .models import AllotmentStatement
from .forms import AllotmentStatementForm


def allotment_list(request):
    fund = request.GET.get('fund', '')
    year = request.GET.get('year', '')

    records = SubAllotmentAdvice.objects.prefetch_related(
        'province_allotments__cis_allotments'
    ).order_by('-date')

    if fund:
        records = records.filter(advice_number__icontains=fund)
    if year:
        records = records.filter(advice_number__icontains=year)

    def extract_years(fund_code):
        nums = SubAllotmentAdvice.objects.filter(
            advice_number__icontains=fund_code
        ).values_list('advice_number', flat=True)
        years = set()
        for num in nums:
            parts = num.split('-')
            for part in parts:
                if part.isdigit() and len(part) == 4:
                    years.add(int(part))
        return sorted(years)

    return render(request, 'nia_app/allotment_list.html', {
        'records': records,
        'active_fund': fund,
        'active_year': year,
        'cob_years':  extract_years('COB'),
        'lfps_years': extract_years('LFPs'),
        'carp_years': extract_years('CARP'),
    })


def allotment_create(request):
    if request.method == 'POST':
        form = AllotmentStatementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Allotment record saved successfully!')
            return redirect('allotment_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = AllotmentStatementForm()
    return render(request, 'nia_app/allotment_form.html', {'form': form, 'title': 'New Allotment Record', 'action': 'Create'})


def allotment_edit(request, pk):
    record = get_object_or_404(AllotmentStatement, pk=pk)
    if request.method == 'POST':
        form = AllotmentStatementForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record updated successfully!')
            return redirect('allotment_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = AllotmentStatementForm(instance=record)
    return render(request, 'nia_app/allotment_form.html', {'form': form, 'title': 'Edit Allotment Record', 'action': 'Update'})


def allotment_delete(request, pk):
    record = get_object_or_404(AllotmentStatement, pk=pk)
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Record deleted.')
        return redirect('allotment_list')
    return render(request, 'nia_app/allotment_confirm_delete.html', {'record': record})


# ── Master Table API Views ────────────────────────────────────────
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import GAASAROMaster, ObjectCodeMaster, DescriptionMaster, AdviceNumberMaster, CISMaster


def api_get_gaa(request):
    items = list(GAASAROMaster.objects.values_list('id', 'value'))
    return JsonResponse({'items': [{'id': i[0], 'value': i[1]} for i in items]})


def api_get_object_codes(request):
    items = list(ObjectCodeMaster.objects.values_list('id', 'value'))
    return JsonResponse({'items': [{'id': i[0], 'value': i[1]} for i in items]})


def api_get_descriptions(request):
    items = list(DescriptionMaster.objects.values_list('id', 'value'))
    return JsonResponse({'items': [{'id': i[0], 'value': i[1]} for i in items]})


def api_get_advice_numbers(request):
    items = list(AdviceNumberMaster.objects.values_list('id', 'value'))
    return JsonResponse({'items': [{'id': i[0], 'value': i[1]} for i in items]})


def api_get_cis(request):
    province = request.GET.get('province', '')
    if province:
        items = CISMaster.objects.filter(province=province).values('id', 'cis_name')
        return JsonResponse({'items': [{'id': i['id'], 'value': i['cis_name']} for i in items]})
    else:
        items = CISMaster.objects.all().values('id', 'province', 'cis_name')
        return JsonResponse({'items': [{'id': i['id'], 'province': i['province'], 'cis_name': i['cis_name']} for i in items]})


@csrf_exempt
def api_save_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            table = data.get('table')
            value = data.get('value', '').strip()
            province = data.get('province', '').strip()

            if not value:
                return JsonResponse({'success': False, 'error': 'Value is required'})

            if table == 'gaa':
                obj, created = GAASAROMaster.objects.get_or_create(value=value)
            elif table == 'object_code':
                obj, created = ObjectCodeMaster.objects.get_or_create(value=value)
            elif table == 'description':
                obj, created = DescriptionMaster.objects.get_or_create(value=value)
            elif table == 'advice_number':
                obj, created = AdviceNumberMaster.objects.get_or_create(value=value)
            elif table == 'cis':
                if not province:
                    return JsonResponse({'success': False, 'error': 'Province is required for CIS'})
                obj, created = CISMaster.objects.get_or_create(province=province, cis_name=value)
            else:
                return JsonResponse({'success': False, 'error': 'Unknown table'})

            return JsonResponse({'success': True, 'id': obj.id, 'value': value, 'created': created})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'POST required'})


def api_get_suballotment_records(request):
    return JsonResponse({'records': []})


def master_lists(request):
    return render(request, 'nia_app/master_lists.html')


@csrf_exempt
def api_delete_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            table = data.get('table')
            item_id = data.get('id')

            if table == 'gaa':
                GAASAROMaster.objects.filter(id=item_id).delete()
            elif table == 'object_code':
                ObjectCodeMaster.objects.filter(id=item_id).delete()
            elif table == 'description':
                DescriptionMaster.objects.filter(id=item_id).delete()
            elif table == 'advice_number':
                AdviceNumberMaster.objects.filter(id=item_id).delete()
            elif table == 'cis':
                CISMaster.objects.filter(id=item_id).delete()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'POST required'})

ITEMS = ['CIVIL WORKS/CONTRACT WORKS', 'FORCE ACCOUNT WORKS/ADMIN WORKS', 'INSTITUTIONAL DEVELOPMENT PROGRAM', 'CONSTRUCTION SURVEY','PARCELLARY MAP', 'FIELD SUPERIOR SUPPORT MONITORING', 'RIGHT OF WAY', 'ENVIRONMENTAL IMPACT C', 'TOTAL']

def province_table(request, office, province):
    asa_number = request.GET.get('asa', '')
    advice = SubAllotmentAdvice.objects.filter(advice_number=asa_number).first()
    
    return render(request, 'nia_app/province_table.html', {
        'office': office,
        'province': province,
        'items': ITEMS,
        'advice': advice,
        'asa_number': asa_number,
    })

@csrf_exempt
def save_province_table(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)

            # ── DELETE ──
            if body.get('delete'):
                advice_pk = body.get('advice_pk')
                office    = body.get('office')
                province  = body.get('province')
                ProgramOfWork.objects.filter(
                    advice_id=advice_pk,
                    office=office,
                    province=province
                ).delete()
                return JsonResponse({'ok': True})

            # ── SAVE ──
            advice_pk = body.get('advice_pk')
            office    = body.get('office')
            province  = body.get('province')
            rows      = body.get('data', [])

            advice = SubAllotmentAdvice.objects.get(pk=advice_pk)
            pow_record, _ = ProgramOfWork.objects.update_or_create(
                advice=advice,
                office=office,
                province=province,
            )

            for idx, row in enumerate(rows):
                item   = row.get('item')
                values = row.get('values', [])
                if item == 'TOTAL':
                    continue
                ProgramOfWorkItem.objects.update_or_create(
                    program=pow_record,
                    item=item,
                    defaults={
                        'pow_amount': values[0] or 0,
                        'imo_amount': values[1] or 0,
                        'mo_amount':  values[2] or 0,
                        'order':      idx,
                    }
                )
            return JsonResponse({'ok': True})

        except SubAllotmentAdvice.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Advice not found'})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)})

    return JsonResponse({'ok': False, 'error': 'Invalid method'})
