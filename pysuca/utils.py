from lxml import etree



XML_NS = '{http://www.w3.org/XML/1998/namespace}'
TEI_NS = '{http://www.tei-c.org/ns/1.0}'


def fetch_ns():
    """
    Return a namespace dict
    """
    return {"tei_ns": TEI_NS,
            "xml_ns": XML_NS}


def parse_tei(_path, get_ns=True):
    """
    Parse a document, return root element (and namespace defnitions).

    Args:

        _path (str): path to tei-xml doc
        get_ns (bool): also return namespace dict

    Returns:

        tuple/etree._Element: root and an optional namespace dict
    """
    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.parse(_path, parser).getroot()
    if get_ns:
        ns = fetch_ns()
        return root, ns
    else:
        return root


def write_tei(elem, file_, padding=8, rm_empty=True):
    """
    Write tei object to a file

    Args

        elem (etree obj): TEI object
        file_ (str): file path+name

    Kwargs

        rm_empty (bool): delete elements with no text (default: False)
    """
    def _iter(root, ns="{http://www.tei-c.org/ns/1.0}"):
        for div in root.findall(f".//{ns}div"):
            for ix, elem in enumerate(div):
                if elem.tag == ns + "u":
                    yield "u", elem
                elif elem.tag == ns + "note":
                    yield "note", elem
                elif elem.tag == ns + "pb":
                    yield "pb", elem
                elif elem.tag == "pb":
                    elem.tag = ns + "pb"
                    yield "pb", elem
                elif elem.tag == ns + "seg":
                    yield "seg", elem
                elif elem.tag == "u":
                    elem.tag = ns + "u"
                    yield "u", elem
                elif elem.tag == "p":
                    elem.tag = ns+"p"
                    yield "p", elem
                elif elem.tag == ns + "p":
                    yield "p", elem
                elif elem.tag == "span":
                    elem.tag = ns+"span"
                    yield "span", elem
                elif elem.tag == ns + "span":
                    yield "span", elem
                elif elem.tag == "title":
                    elem.tag = ns+"title"
                    yield "title", elem
                elif elem.tag == ns + "title":
                    yield "title", elem
                elif elem.tag == "head":
                    elem.tag = ns+"head"
                    yield "head", elem
                elif elem.tag == ns + "head":
                    yield "head", elem
                else:
                    warnings.warn(f"Unrecognized element {elem.tag}")
                    yield None

    def _format_paragraph(paragraph, spaces):
        s = "\n" + " " * spaces
        words = paragraph.replace("\n", "").strip().split()
        row = ""
        for word in words:
            if len(row) > 60:
                s += row.strip() + "\n" + " " * spaces
                row = word
            else:
                row += " " + word
        if len(row.strip()) > 0:
            s += row.strip() + "\n" + " " * (spaces - 2)
        if s.strip() == "":
            return None
        return s

    def _format_texts(root, rm_empty, padding=12):
        def _format(elem, rm_empty, padding=12):
            if type(elem.text) == str and elem.text is not None and len(elem.text.strip()) > 0:
                elem.text = _format_paragraph(elem.text, padding+2)
                print("  ", elem.text)
            for child in elem:
                print("  ", len(child))
                child = _format(child, rm_empty, padding=padding+2)
            if elem.text == None and len(elem) == 0 and rm_empty:
                elem.getparent().remove(elem)

        for tag, elem in _iter(root):
            print(elem)
            elem = _format(elem, rm_empty, padding=padding)

        return root

    elem = _format_texts(elem, rm_empty, padding=padding)
    b = etree.tostring(
        elem,
        pretty_print=True,
        encoding="utf-8",
            xml_declaration=True
        )
    with open(file_, "wb") as f:
        f.write(b)

