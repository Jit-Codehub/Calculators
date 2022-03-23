from django.urls import path,include
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
]
