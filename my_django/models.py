
# from django.db import models
# from django.contrib.auth.models import User


# class Ingredient(models.Model):
#     #재료테이블은 모든 재료의 이름만 모아놓은 목록
#     """재료 테이블"""
#     name = models.CharField(max_length=50,unique=True)

#     def __str__(self):
#         return self.name


# class Recipe(models.Model):
#     #레시피테이블은 요리에 대한 정보담고 있는 곳
#     """레시피 테이블   """

#     DIFFICULTY_CHOICES = [('쉬움', '쉬움'),('보통', '보통'),('어려움', '어려움'),]

#     title = models.CharField(max_length=100)
#     instructions = models.TextField(help_text="조리 방법")
#     difficulty = models.CharField(max_length=10,choices=DIFFICULTY_CHOICES)
#     prep_time = models.PositiveIntegerField(help_text="조리 시간 (분 단위)")
#     ingredients = models.ManyToManyField(Ingredient,through='RecipeIngredient',related_name='recipes')
#     created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='recipes') #set_null은 연결만 끊고 기록은 남기는방법
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title


# class RecipeIngredient(models.Model):
#     #어떤 레시피에 어떤재료가 얼마나 들어가는지 기록하는 테이블
#     """레시피-재료 중간 테이블"""

#     recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE,related_name='recipe_ingredients')
#     ingredient = models.ForeignKey(Ingredient,on_delete=models.CASCADE,related_name='ingredient_recipes')
#     quantity = models.CharField(max_length=30,help_text="예: 1개, 2큰술, 약간")
#     is_optional = models.BooleanField(default=False,help_text="선택 재료 여부")

#     class Meta:
#         unique_together = ('recipe', 'ingredient')

#     def __str__(self):
#         return f"{self.recipe.title} : {self.ingredient.name}"


# class RefrigeratorIngredient(models.Model):
#     """사용자 냉장고 재료"""

#     user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='refrigerator_ingredients')
#     ingredient = models.ForeignKey(Ingredient,on_delete=models.CASCADE)
#     quantity = models.CharField(max_length=30,blank=True,help_text="예: 2개, 반 봉지")
#     expiry_date = models.DateField(null=True, blank=True, help_text="유통기한")

#     added_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'ingredient')
#         ordering = ['expiry_date'] #유통기한 임박순으로 정렬

#     def __str__(self):
#         #이름:재료이름(수량)으로 표현
#         return f"{self.user.username} : {self.ingredient.name} ({self.quantity})"