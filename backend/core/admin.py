from django.contrib import admin
from django_admin_hstore_widget.forms import HStoreFormField
from django import forms

from core.models.geo_unit import GeoUnit, GeoUnitType
from core.models.individual_care import IndividualCategory, IndividualCare, IndividualCareCategory
from core.models.data_import import DataImportLog, DataImportParam, DataImportProfile, DataImportCategory


# Register your models here.
class GeoUnitAdmin(admin.ModelAdmin):
    model = GeoUnit
    list_display = ('name', 'type', 'ibge', 'cnes', 'parent', 'description', 'latitude', 'longitude')
    search_fields = ('name', 'parent__name', 'type__name')
    list_filter = ('type',)


admin.site.register(GeoUnit, GeoUnitAdmin)


class GeoUnitTypeAdmin(admin.ModelAdmin):
    model = GeoUnitType
    search_fields = ('name',)
    list_display = ('name', 'description')


admin.site.register(GeoUnitType, GeoUnitTypeAdmin)


# Inline para exibir as categorias relacionadas ao cuidado individual
class IndividualCareCategoryInline(admin.TabularInline):
    model = IndividualCareCategory
    extra = 1
    autocomplete_fields = ['individual_category']


# Filtro personalizado para filtrar por categoria
class CategoryFilter(admin.SimpleListFilter):
    title = 'Categoria'  # Título do filtro exibido no admin
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        """Define as opções de filtro disponíveis."""
        categories = IndividualCategory.objects.all()
        return [(category.id, category.name) for category in categories]

    def queryset(self, request, queryset):
        """Filtra o queryset com base na categoria selecionada."""
        if self.value():
            return queryset.filter(individualcarecategory__individual_category_id=self.value())
        return queryset


# Filtro personalizado para GeoUnit mostrando apenas os tipos específicos
# Admin para o modelo IndividualCare
@admin.register(IndividualCare)
class IndividualCareAdmin(admin.ModelAdmin):
    list_display = ['geo_unit', 'year', 'month', 'group_param', 'class_param']
    search_fields = ['geo_unit__name', 'year']
    inlines = [IndividualCareCategoryInline]
    list_filter = [CategoryFilter]  # Adiciona o filtro personalizado por categoria

    def get_categories(self, obj):
        """Exibe as categorias relacionadas a um cuidado individual."""
        return ", ".join([str(category.individual_category.name) for category in obj.individualcarecategory_set.all()])

    get_categories.short_description = 'Categorias'


# Admin para o modelo IndividualCategory
@admin.register(IndividualCategory)
class IndividualCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


# Admin para o modelo IndividualCareCategory
# @admin.register(IndividualCareCategory)
# class IndividualCareCategoryAdmin(admin.ModelAdmin):
#     list_display = ['individual_care', 'individual_category']
#     search_fields = ['individual_care__geo_unit__name', 'individual_category__name']


class DataImportParamAdminForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    value = HStoreFormField()
    active = forms.BooleanField(required=False)

    class Meta:
        model = DataImportParam
        exclude = ()


class DataImportParamInline(admin.TabularInline):
    model = DataImportParam
    extra = 1
    # form = DataImportParamAdminForm


class DataImportProfileAdmin(admin.ModelAdmin):
    model = DataImportProfile
    list_display = ['name', 'description', 'active', 'data_import_category']
    search_fields = ['name', 'data_import_category']
    list_filter = ('data_import_category',)

    inlines = [DataImportParamInline]


admin.site.register(DataImportProfile, DataImportProfileAdmin)


class DataImportLogAdmin(admin.ModelAdmin):
    model = DataImportLog
    list_display = ['file_name', 'import_date', 'get_status_display', 'message']

    # Método personalizado para mostrar o status
    def get_status_display(self, obj):
        return obj.get_status_display()

    get_status_display.short_description = 'Status'


admin.site.register(DataImportLog, DataImportLogAdmin)


@admin.register(DataImportParam)
class DataImportParamAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']
    form = DataImportParamAdminForm


@admin.register(DataImportCategory)
class DataImportCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    model = DataImportCategory
