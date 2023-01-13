import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Adesso Showcases")
# Sidebar
st.sidebar.title("Adesso Data & Analytics")
# Sidebar display logo
st.sidebar.text("CC AI & Data Science")
st.sidebar.image("detection/ressources/white.png", use_column_width=True)
st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Adesso SE ist ein führendes Beratungs- und IT-Dienstleistungsunternehmen,
     das sich darauf spezialisiert hat, Unternehmen durch innovative Ideen, zukunftsfähige Strategien und
     passgenaue IT-Lösungen bei ihren individuellen Herausforderungen zu unterstützen. Dabei steht das Unternehmen
     für den Ansatz "business. people. technology.", was bedeutet, dass erfolgreiches Geschäft durch den richtigen
     Mix aus Technologieexpertise und fundiertem Verständnis für das jeweilige Geschäft der Kunden entsteht.

Mit einem Team von über 7.500 Mitarbeiterinnen und Mitarbeitern arbeitet Adesso an 57 Standorten innerhalb der adesso Group
 als einer der führenden IT-Dienstleister im deutschsprachigen Raum.
Das Unternehmen hat sich auf die Kernbranchen Versicherungen/Rückversicherungen, Banken/Finanzdienstleistungen, Gesundheitswesen,
Öffentliche Verwaltung, Automobilindustrie, Maschinenbau und Fertigungstechnik, Handel sowie Energie- und Wasserwirtschaft spezialisiert.
Adesso ist in der Lünendonk-Liste 2022 auf Platz 11 von 25 der führenden IT-Beratungs- und Systemintegrations-Unternehmen in Deutschland gelistet.
 Das Unternehmen hatte 2020 bereits Platz 1 erreicht, bevor es das Größenkriterium für die Liste der 25 führenden mittelständischen IT-Beratungen überschritten hat.

Adesso ist bekannt für seine umfassenden Lösungen und sein engagiertes Team von Fachleuten, das Unternehmen und Organisationen
dabei unterstützt, ihre Geschäftsprozesse durch den Einsatz von Technologie zu optimieren und ihre Ziele zu erreichen. Mit seinem breiten
Leistungsspektrum und seiner langjährigen Erfahrung hat sich das Unternehmen einen hervorragenden Ruf erworben und gehört zu den angesehensten
 IT-Dienstleistern in Deutschland.





"""
)
