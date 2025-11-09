"""
Visualization example using IDent.

This example shows how to:
1. Analyze multiple texts
2. Create 2D visualizations (PCA, t-SNE)
3. Create feature comparison plots
4. Create similarity heatmaps
"""

from ident import StyleAnalyzer
from ident.visualizer import (
    visualize_profiles_2d,
    plot_feature_comparison,
    plot_similarity_heatmap,
    plot_radar_chart
)

# Sample texts with different styles (expanded for better analysis)
texts = {
    "News": """
    Sveriges ekonomi växer stadigt enligt nya rapporter från Statistiska centralbyrån.
    Tillväxten under det senaste kvartalet uppgick till 2,3 procent, vilket är högre än
    väntat. Experter menar att den starka arbetsmarknaden och ökade investeringar i
    infrastruktur bidrar till den positiva utvecklingen. Samtidigt varnar ekonomer för
    att inflationen fortsätter att vara en utmaning. Konsumentpriserna har stigit mer
    än förväntat, vilket påverkar hushållens köpkraft negativt. Riksbanken överväger
    ytterligare räntehöjningar för att dämpa prisökningstakten. Den svenska kronan har
    försvagats mot euron under den senaste månaden, vilket gynnar exportföretagen men
    gör importerade varor dyrare. Många företag inom tillverkningsindustrin rapporterar
    starka orderingångar från utlandet. Arbetslösheten ligger kvar på en låg nivå.
    """,

    "Blog": """
    Hej allihopa! Idag måste jag bara berätta om mitt nya favoritcafé! Det är så mysigt där.
    Atmosfären är helt underbar och personalen är superschysst. Jag brukar ta en cappuccino
    och en kanelbulle när jag är där. Mums! Det är verkligen det bästa stället att hänga på.
    Alla mina vänner älskar det också. Vi träffas där minst en gång i veckan. Ibland sitter
    vi där i timmar och bara snackar och skrattar. Det är så skönt att bara koppla av lite.
    Livet är ju så stressigt annars! Man måste ta sig tid för sådana här stunder. Förra
    veckan provade jag deras nya smoothie. Den var jättegod! Jag rekommenderar verkligen
    detta ställe till alla som letar efter ett nice café i stan. Fem stjärnor från mig!
    """,

    "Academic": """
    Analys av samtida svenska språkförändring visar på flera intressanta fenomen.
    Forskningen indikerar att digitaliseringen har påverkat språkbruket signifikant,
    särskilt bland yngre generationer. Syntaktiska strukturer förenklas, medan lexikala
    lån från främst engelskan ökar i frekvens. Morfologiska förändringar observeras i
    böjningsmönster, där traditionella genussystem gradvis eroderar. Pragmatiska aspekter
    av språkanvändning uppvisar komplexare mönster än tidigare dokumenterat.
    Diskursanalytiska undersökningar belyser hur interaktionella strategier transformerats
    i digitala miljöer. Metodologiskt tillämpas multimodala analysramverk för att
    fånga kommunikationens flerfaldigade dimensioner i nutida medielandskap. Resultaten
    tyder på systematiska variationsmönster korrelerade med sociodemografiska variabler.
    """,

    "Fiction": """
    Solen gick sakta ner över horisonten och målade himlen i vackra nyanser av rött och
    orange. Emma stod vid stranden och lät vågorna skölja över hennes bara fötter. Det
    kändes befriande. Allt det där med jobbet, alla bekymmer - det spelade ingen roll
    just nu. Hon andades djupt och njöt av havsluften. Måsarna skrek högt ovanför henne.
    Några barn lekte längre bort på stranden. Deras skratt ekade mellan klipporna. Emma
    log för sig själv. Hon tänkte på sommaren som barn, när allt kändes så enkelt och
    ljust. Nu var livet mer komplicerat, men ögonblick som dessa påminde henne om vad
    som verkligen var viktigt. Friheten. Kärleken. Naturen. Hon bestämde sig för att
    komma hit oftare. Detta var hennes plats, hennes tillflykt från vardagens stress.
    """,
}

# Initialize analyzer
print("Initializing StyleAnalyzer...")
analyzer = StyleAnalyzer()

# Analyze all texts
print("Analyzing texts...")
profiles = []
for name, text in texts.items():
    profile = analyzer.analyze(text, name=name)
    profiles.append(profile)
    print(f"  ✓ {name}")

print(f"\nCreated {len(profiles)} profiles")
print("\nGenerating visualizations...\n")

# 1. PCA visualization
print("Creating PCA visualization...")
visualize_profiles_2d(
    profiles,
    method='pca',
    title='Swedish Text Styles - PCA',
    save_path='pca_comparison.png'
)

# 2. t-SNE visualization
print("\nCreating t-SNE visualization...")
visualize_profiles_2d(
    profiles,
    method='tsne',
    title='Swedish Text Styles - t-SNE',
    perplexity=3,  # Adjusted for small dataset
    save_path='tsne_comparison.png'
)

# 3. Feature comparison
print("\nCreating feature comparison plot...")
plot_feature_comparison(
    profiles,
    top_n=10,
    save_path='feature_comparison.png'
)

# 4. Similarity heatmap
print("\nCreating similarity heatmap...")
plot_similarity_heatmap(
    profiles,
    method='cosine',
    save_path='similarity_heatmap.png'
)

# 5. Radar chart
print("\nCreating radar chart...")
plot_radar_chart(
    profiles,
    top_n=8,
    save_path='radar_comparison.png'
)

print("\n" + "="*60)
print("All visualizations completed!")
print("="*60)
print("\nGenerated files:")
print("  - pca_comparison.png")
print("  - tsne_comparison.png")
print("  - feature_comparison.png")
print("  - similarity_heatmap.png")
print("  - radar_comparison.png")
