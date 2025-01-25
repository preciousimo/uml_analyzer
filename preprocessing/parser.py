from lxml import etree

def parse_xmi(xmi_file):
    """
    Parse a UML diagram in XMI format and extract relevant elements.
    """
    tree = etree.parse(xmi_file)
    root = tree.getroot()

    # Extract Use Case Diagram elements
    use_cases = root.xpath("//uml:UseCase", namespaces=root.nsmap)
    actors = root.xpath("//uml:Actor", namespaces=root.nsmap)

    # Extract Class Diagram elements
    classes = root.xpath("//uml:Class", namespaces=root.nsmap)
    associations = root.xpath("//uml:Association", namespaces=root.nsmap)

    return {
        "use_cases": [{"name": uc.get("name"), "description": uc.get("description")} for uc in use_cases],
        "actors": [{"name": actor.get("name")} for actor in actors],
        "classes": [{"name": cls.get("name"), "methods": cls.xpath(".//uml:Operation/@name", namespaces=root.nsmap)} for cls in classes],
        "associations": [{"source": assoc.get("source"), "target": assoc.get("target")} for assoc in associations]
    }