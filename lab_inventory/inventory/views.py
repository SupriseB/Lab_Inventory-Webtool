from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Category, Item
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum, Count


# ---------------- Categories ----------------
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'inventory/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'inventory/category_form.html'
    success_url = reverse_lazy('category-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'inventory/category_form.html'
    success_url = reverse_lazy('category-list')

    def test_func(self):
        category = self.get_object()
        return self.request.user == category.user

class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'inventory/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')

    def test_func(self):
        category = self.get_object()
        return self.request.user == category.user


# ---------------- Items ----------------

class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'inventory/item_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        queryset = Item.objects.filter(user=self.request.user).select_related('category')

        # --- Search ---
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)

        # --- Filter by category ---
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category__id=category_id)

        # --- Sorting ---
        sort_by = self.request.GET.get('sort', 'name')  # default sort by name
        if sort_by in ['name', 'quantity', 'purchase_date']:
            queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(user=self.request.user)
        return context
    

# ---------------- Items ----------------

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['name', 'description', 'quantity', 'reorder_level', 'location', 'category', 'purchase_date']
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('item-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = ['name', 'description', 'quantity', 'reorder_level', 'location', 'category', 'purchase_date']
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('item-list')

    def test_func(self):
        item = self.get_object()
        return self.request.user == item.user


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    template_name = 'inventory/item_confirm_delete.html'
    success_url = reverse_lazy('item-list')

    def test_func(self):
        item = self.get_object()
        return self.request.user == item.user

    


#........Dashboard..........................

@login_required
def dashboard(request):
    items = Item.objects.filter(user=request.user)

    total_items = items.count()
    total_quantity = items.aggregate(Sum('quantity'))['quantity__sum'] or 0
    low_stock_count = items.filter(quantity__lte=F('reorder_level')).count()
    category_summary = (
        items.values('category__name')
             .annotate(total=Count('id'))
             .order_by('category__name')
    )

    context = {
        "total_items": total_items,
        "total_quantity": total_quantity,
        "low_stock_count": low_stock_count,
        "category_summary": category_summary,
    }
    return render(request, "inventory/dashboard.html", context)
#...........Inventory Data Exportation.................
#For Full stock
#CSV
import csv
from django.http import HttpResponse



@login_required
def export_csv(request):
    items = Item.objects.filter(user=request.user)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Description', 'Quantity', 'Purchase Date', 'Location', 'Category'])

    for item in items:
        writer.writerow([
            item.name,
            item.description,
            item.quantity,
            item.purchase_date,
            item.location,
            item.category.name if item.category else ""
        ])

    return response
#PDF
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from .models import Item

def export_pdf(request):
    items = Item.objects.filter(user=request.user)

    # Setup response
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="inventory_report.pdf"'

    # PDF document
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("📊 Laboratory Inventory Report", styles["Title"]))
    elements.append(Spacer(1, 20))

    # Table data
    data = [["Name", "Category", "Quantity", "Reorder Level", "Location", "Purchase Date"]]

    for item in items:
        data.append([
            item.name,
            item.category.name if item.category else "Uncategorized",
            item.quantity,
            item.reorder_level,
            item.location,
            item.purchase_date.strftime("%Y-%m-%d"),
        ])

    # Create table
    table = Table(data, colWidths=[100, 100, 60, 80, 100, 80])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#007bff")),  # blue header
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
    ]))

    elements.append(table)

    # Build PDF
    doc.build(elements)

    return response


#For Low stock
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Item
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# ---------------- CSV Export for Low Stock ----------------
def export_lowstock_csv(request):
    lowstock_items = Item.objects.filter(quantity__lte=5)  # adjust threshold if needed
    
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="low_stock_items.csv"'
    
    # Write CSV manually
    import csv
    writer = csv.writer(response)
    writer.writerow(["Name", "Category", "Quantity", "Reorder Level", "Location"])
    
    for item in lowstock_items:
        writer.writerow([
            item.name,
            item.category.name if item.category else "Uncategorized",
            item.quantity,
            item.reorder_level,
            item.location
        ])
    
    return response


# ---------------- PDF Export for Low Stock ----------------


def export_lowstock_pdf(request):
    lowstock_items = Item.objects.filter(quantity__lte=5)

    # Setup response
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="low_stock_items.pdf"'

    # PDF document
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("⚠️ Low Stock Items Report", styles["Title"]))
    elements.append(Spacer(1, 20))

    # Table data
    data = [["Name", "Category", "Quantity", "Reorder Level", "Location"]]  # headers

    for item in lowstock_items:
        data.append([
            item.name,
            item.category.name if item.category else "Uncategorized",
            item.quantity,
            item.reorder_level,
            item.location,
        ])

    # Create table
    table = Table(data, colWidths=[120, 100, 60, 100, 100])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f44336")),  # red header
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
    ]))

    elements.append(table)

    # Build PDF
    doc.build(elements)

    return response
