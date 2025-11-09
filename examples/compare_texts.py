"""
Text comparison example using IDent.

This example shows how to:
1. Analyze multiple Swedish texts
2. Compare their styles
3. Find distinctive features
"""

from ident import StyleAnalyzer
from ident.comparator import find_most_similar, get_distinctive_features

# Sample texts with different styles

# Formal news/report style
text1 = """
Sveriges ekonomi växer stadigt enligt nya rapporter från Statistiska centralbyrån.
Tillväxten under det senaste kvartalet uppgick till 2,3 procent, vilket är högre än
väntat. Experter menar att den starka arbetsmarknaden och ökade investeringar i
infrastruktur bidrar till den positiva utvecklingen. Samtidigt varnar ekonomer för
att inflationen fortsätter att vara en utmaning. Konsumentpriserna har stigit mer
än förväntat, vilket påverkar hushållens köpkraft negativt. Riksbanken överväger
ytterligare räntehöjningar för att dämpa prisökningstakten. Den svenska kronan har
försvagats mot euron under den senaste månaden, vilket gynnar exportföretagen men
gör importerade varor dyrare. Många företag inom tillverkningsindustrin rapporterar
starka orderingångar från utlandet. Arbetslösheten ligger kvar på en låg nivå, men
det råder brist på kvalificerad arbetskraft inom flera sektorer.
"""

# Informal blog/conversational style
text2 = """
Hallå där! Idag tänkte jag prata lite om min favoriträtt - pannkakor! Gud vad gott
det är. Jag älskar verkligen att äta pannkakor, särskilt med sylt och grädde. Mums!
När jag var liten åt vi pannkakor varje torsdag. Det var ju tradition, eller hur?
Mamma stod alltid vid spisen och vände dem så försiktigt. Ibland blev de lite
brända, men det gjorde inget. Vi åt dem ändå! Nuförtiden gör jag egna pannkakor
hemma. Det är faktiskt superenkelt! Man bara blandar mjöl, mjölk, ägg och lite salt.
Sen steker man dem i smör. Jag brukar göra riktigt många så att det blir över till
dagen efter. Pannkaksrullar är också supergott! Man rullar ihop pannkakorna med
sylt inuti. Perfekt mellanmål! Mina barn älskar också pannkakor. De hjälper till
att blanda smeten ibland. Det blir alltid lite stök i köket, men det är kul ändå!
"""

# Academic/analytical style
text3 = """
Analys av samtida svenska språkförändring visar på flera intressanta fenomen.
Forskningen indikerar att digitaliseringen har påverkat språkbruket signifikant,
särskilt bland yngre generationer. Syntaktiska strukturer förenklas, medan lexikala
lån från främst engelskan ökar. Morfologiska förändringar observeras i böjningsmönster,
där traditionella genussystem gradvis eroderar. Samtidigt noteras en ökad variation
i ortografi, delvis beroende på informella digitala kommunikationsformer. Studier
påvisar att språklig prestigehierarki förändras, med dialektala och sociolektala
variabler som tidigare stigmatiserats nu accepteras i fler kontexter. Pragmatiska
aspekter av språkanvändning uppvisar komplexare mönster än tidigare dokumenterat.
Diskursanalytiska undersökningar belyser hur interaktionella strategier transformerats
i digitala miljöer. Metodologiskt tillämpas multimodala analysramverk för att fånga
kommunikationens flerfaldigade dimensioner i nutida medielandskap.
"""

# Initialize analyzer
print("Initializing StyleAnalyzer...")
analyzer = StyleAnalyzer()

# Analyze all texts
print("\nAnalyzing texts...")
profiles = analyzer.analyze_multiple(
    texts=[text1, text2, text3],
    names=["News Article", "Blog Post", "Academic Text"]
)

print(f"Created {len(profiles)} profiles\n")

# Compare profiles pairwise
print("="*60)
print("Pairwise Comparisons (Cosine Similarity):")
print("="*60)

for i in range(len(profiles)):
    for j in range(i+1, len(profiles)):
        similarity = profiles[i].compare(profiles[j], method='cosine')
        print(f"{profiles[i].name} vs {profiles[j].name}: {similarity:.3f}")

print()

# Find distinctive features between two texts
print("="*60)
print("Most Distinctive Features (News vs Blog):")
print("="*60)

distinctive = get_distinctive_features(profiles[0], profiles[1], top_n=10)

for feature, (val1, val2, diff) in distinctive.items():
    feature_name = feature.replace('_', ' ').title()
    print(f"{feature_name:.<45}")
    print(f"  News Article: {val1:.4f}")
    print(f"  Blog Post:    {val2:.4f}")
    print(f"  Difference:   {diff:.4f}")
    print()

# Find most similar profiles
print("="*60)
print("Most Similar to News Article:")
print("="*60)

similar = find_most_similar(profiles[0], profiles, method='cosine', top_n=2)

for profile, similarity in similar:
    print(f"{profile.name}: {similarity:.3f}")
