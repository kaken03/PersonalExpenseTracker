from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Expense
from .forms import ExpenseForm

@login_required(login_url='login')
def dashboard(request):
    """Display user dashboard with monthly total and recent expenses."""
    user_expenses = Expense.objects.filter(user=request.user)
    
    # Get current month and year
    today = timezone.now().date()
    current_month_start = today.replace(day=1)
    
    # Calculate monthly total
    monthly_expenses = user_expenses.filter(
        date__year=today.year,
        date__month=today.month
    )
    monthly_total = monthly_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Get recent 5 expenses
    recent_expenses = user_expenses[:5]
    
    context = {
        'monthly_total': monthly_total,
        'recent_expenses': recent_expenses,
        'expense_count': user_expenses.count(),
    }
    return render(request, 'expenses/dashboard.html', context)

@login_required(login_url='login')
def expense_list(request):
    """Display all user expenses with filtering by category."""
    user_expenses = Expense.objects.filter(user=request.user)
    
    # Filter by category if provided
    category = request.GET.get('category')
    if category:
        user_expenses = user_expenses.filter(category=category)
    
    # Search by description
    search = request.GET.get('search')
    if search:
        user_expenses = user_expenses.filter(description__icontains=search)
    
    context = {
        'expenses': user_expenses,
        'categories': Expense.CATEGORY_CHOICES,
        'selected_category': category,
        'search_query': search,
    }
    return render(request, 'expenses/expense_list.html', context)

@login_required(login_url='login')
def expense_create(request):
    """Create a new expense."""
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            
            # Check if AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'expense': {
                        'id': expense.id,
                        'date': expense.date.strftime('%Y-%m-%d'),
                        'category': expense.get_category_display(),
                        'category_code': expense.category,
                        'amount': str(expense.amount),
                        'description': expense.description if expense.description else '',
                        'created_at': expense.created_at.strftime('%b %d, %Y %I:%M %p'),
                    }
                })
            return redirect('expense_list')
        else:
            # Check if AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Convert form errors to dictionary of lists
                errors = {}
                for field, field_errors in form.errors.items():
                    errors[field] = [str(error) for error in field_errors]
                return JsonResponse({
                    'status': 'error',
                    'errors': errors
                }, status=400)
    else:
        form = ExpenseForm()
    
    context = {'form': form, 'title': 'Add Expense'}
    return render(request, 'expenses/expense_form.html', context)

@login_required(login_url='login')
def expense_detail(request, pk):
    """Display expense detail."""
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    return render(request, 'expenses/expense_detail.html', {'expense': expense})

@login_required(login_url='login')
def expense_update(request, pk):
    """Update an existing expense."""
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            
            # Check if AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'expense': {
                        'id': expense.id,
                        'date': expense.date.strftime('%Y-%m-%d'),
                        'category': expense.get_category_display(),
                        'category_code': expense.category,
                        'amount': str(expense.amount),
                        'description': expense.description if expense.description else '',
                        'created_at': expense.created_at.strftime('%b %d, %Y %I:%M %p'),
                    }
                })
            return redirect('expense_list')
        else:
            # Check if AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Convert form errors to dictionary of lists
                errors = {}
                for field, field_errors in form.errors.items():
                    errors[field] = [str(error) for error in field_errors]
                return JsonResponse({
                    'status': 'error',
                    'errors': errors
                }, status=400)
    else:
        form = ExpenseForm(instance=expense)
    
    context = {'form': form, 'expense': expense, 'title': 'Edit Expense'}
    return render(request, 'expenses/expense_form.html', context)

@login_required(login_url='login')
def expense_delete(request, pk):
    """Delete an expense."""
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    
    if request.method == 'POST':
        expense_id = expense.id
        expense.delete()
        
        # Check if AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Expense deleted successfully',
                'expense_id': expense_id
            })
        return redirect('expense_list')
    
    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})
