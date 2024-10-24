from ninja import Router
from typing import List
from inventory.models import Category
from .schema import SuccessMessageSchema, NotFoundSchema, CategorySchema

router = Router()

@router.post("/add-supplier-category", tags=["For Admin"], auth = None, response={200: SuccessMessageSchema, 404: NotFoundSchema})
def add_supplier_category(request, name: str):
    try:
        if Category.objects.filter(name = name).exists():
            return 404, {"message": "Category name already exists"}
        category = Category.objects.create(name = name)
        if category:
            return 200, {"message": "Category has been created"}
    
    except Exception as e:
        return 404, {"message": "We ran into error while processing your request."}
    
@router.get("/list-supplier-categories", tags=["For Admin"], auth = None, response={200: List[CategorySchema], 404: NotFoundSchema})
def list_supplier_categories(request):
    category_list = Category.objects.all()
    return category_list