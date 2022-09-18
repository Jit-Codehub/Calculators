from django.urls import path,include, re_path
from App import sitemaps, views
from django.contrib.sitemaps.views import sitemap
from App.sitemaps import StaticStie, AddSite, SubSite, MultiplySite, DivisionSite

sitemaps = {
    'sitemap':StaticStie,
    'AddSite':AddSite,
    'SubSite':SubSite,
    'MultiplySite':MultiplySite,
    'DivisionSite':DivisionSite
}
urlpatterns = [
path('sitemap.xml',sitemap, {'sitemaps':sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
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

path("addition-table-generator/", views.additiontablegeneratorcalculator, name="addG"),
path("subtraction-table-generator/", views.subtractiontablegeneratorcalculator, name="subG"),
path("multiplication-table-generator/", views.multiplicationtablegeneratorcalculator, name="mulG"),
path("division-table-generator/", views.divisiontablegeneratorcalculator, name="divG"),

# re_path(r"^addition-table(?:-of-(?P<a>[0-9]+))?/$", views.additiontablegeneratorcalculator, name='add'),

path("addition-table-of-<int:a>/", views.additiontablegeneratorcalculator, name='add'),
path("subtraction-table-of-<int:a>/", views.subtractiontablegeneratorcalculator, name= 'sub'),
path("multiplication-table-of-<int:a>/", views.multiplicationtablegeneratorcalculator, name= 'multiply'),
path("division-table-of-<int:a>/", views.divisiontablegeneratorcalculator, name= 'division'),

path("alfven-velocity-calculator/",views.alfvenvelocitycalculator, name= 'alfven'),
path("terminal-velocity-calculator/",views.terminalvelocitycalculator, name= 'terminal'),
path("pendulum-kinetic-energy-calculator/",views.pendulumkineticenergy, name= 'Pkinetic'),
path("atoms-to-moles-calculator/",views.atomstomolescalculator, name = "atoms"),
path("equivalent-mass-of-acid-calculator/",views.equivalentmassofacidcalculator, name = "acid"),
path("mg-per-ml-to-molarity-calculator/",views.mgmlmolarity, name="mg"),
path("molar-ratio-calculator/",views.molarratiocalculator, name="molar"),
path("mass-from-volume-and-concentration/",views.massfromvolume),
path("volume-from-mass-and-concentration/", views.volumemass),
path("percent-composition-calculator/", views.percentcomposition),
path("impulse-with-time-calculator/", views.impulsewithtime),
path("inductance-calculator/", views.inductancecalculator),
path("solid-waste-moisture-content-calculator/", views.solidwastemoisturecontent),
path("geotextile-permittivity-calculator/", views.geotextilepermittivity),
path("thrust-block-calculator/", views.thrustblock),
path("gold-weight-calculator/", views.goldweightcalculator),
path("earth-orbit-calculator/", views.earthorbitcalculator),
# path("sunrise-sunset-calculator/", views.sunrisesunsetcalculator),
path("f-l-a-m-e-s-calculator/",views.flames),


]


