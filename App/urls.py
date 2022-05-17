from django.urls import path,include, re_path
from App import views
urlpatterns = [
 path('ohms-law-calculator/',views.ohmslawcalculator),
 path('acceleration-of-particle-in-electric-field-calculator/',views.accelerationofparticleinelectricfield), 
 path('momentum-with-time-calculator/',views.momentumwithtimecalculator),
 path('weight-other-planets/',views.weightotherplanets),
 path('specific-heat-calculator/',views.specificheatcalculator), 
 path('half-life-calculator/',views.halflifecalculator),
 path('wet-bulb-calculator/',views.wetbulbcalculator),
 path('arrow-speed-calculator/',views.arrowspeedcalculator),
 path('friction-loss-calculator/',views.frictionlosscalculator),
 path('voltage-divider-calculator/',views.voltagedividercalculator),
 path('frequency-calcultor/',views.frequencycalcultor),
 path('circular-velocity-calculator/',views.circularvelocitycalculator),
 path('engine-horsepower-calculator/',views.enginehorsepowercalculator), 
 path('equivalent-resistance-calculator/',views.equivalentresistancecalculator),
 path('effective-noise-temperature-calculator/',views.noisetemperaturecalculator),
 path('doppler-shift-calculator/',views.dopplershiftcalculator),
 path('clausius-clapeyron-equation-calculator/',views.clausiusclapeyronequationcalculator),
 path('matrix-calculator/',views.matrixcalculator),
 
 path('recursive-sequence-calculator/',views.recursivesequencecalculator),

path('sequence-of-partial-sums-calculator/',views.sequenceofpartialsumscalculator),
path('volumetric-calculator/',views.volumetriccalculator),
path('freight-class-calculator/',views.freightclasscalculator),
path('repeating-decimal-to-fraction-calculator/', views.repeatingdecimaltofractioncalculator),
path('alternative-fuels-conversion-calculator/', views.alternativefuelsconversioncalculator),
path('rgb-hex-conversion-calculator/', views.rgbhexcalculator),
path('inside-car-temperature-calculator/', views.insidecartemperaturecalculator),
path('rain-to-snow-calculator/', views.raintosnowcalculator),
path('snow-calculator/', views.snowcalculator),
path('rainwater-collection-calculator/', views.rainwatercollectioncalculator),
path('estimated-time-of-arrival-calculator/', views.estimatedtimeofarrivalcalculator),
path('english-learning-time-calculator/', views.englishlearningtimecalculator),
path('meeting-cost-calculator/', views.meetingcostcalculator),
path('lead-time-calculator/', views.leadtimecalculator),
path('hair-growth-calculator/', views.hairgrowthcalculator),
path('shower-cost-calculator/', views.showercostcalculator),
path('sunscreen-calculator/', views.sunscreencalculator),
path('bath-vs-shower-calculator/', views.bathvsshowercalculator),
path('jeans-size-calculator/', views.jeanssizecalculator),
path("lost-socks-calculator", views.lostsockscalculator),
path("pleated-skirt-calculator", views.pleatedskirtcalculator),
path("quilt-binding-calculator", views.quiltbindingcalculator),
path("quilt-calculator", views.quiltcalculator),
path("cash-back-or-low-interest-calculator", views.cashbackorlowinterestcalculator),
path("addition-table-generator-calculator", views.additiontablegeneratorcalculator, name='add'),
path("multiplication-table-generator-calculator", views.multiplicationtablegeneratorcalculator, name= 'multiply'),
path("subtraction-table-generator-calculator", views.subtractiontablegeneratorcalculator, name= 'sub'),
path("division-table-generator-calculator", views.divisiontablegeneratorcalculator, name= 'division'),
path('testing', views.testing),
# path('testing/divisoion-of-<int:a>', views.testing, name = "testing"),
re_path(r'^testing/divisoion-of-(?P<a>[0-9][1-9])$', views.testing, name = "testing"),

]
#re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
# 'testing/divisoion\\-of\\-(?P<a>[0-9]+)\\Z'
