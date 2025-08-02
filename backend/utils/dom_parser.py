from bs4 import BeautifulSoup

def extract_dom_summary(dom_html: str) -> str:
    """
    Extracts a simplified summary of the DOM: inputs, buttons, IDs, labels.
    This is useful for building a prompt that guides the LLM.
    """
    soup = BeautifulSoup(dom_html, "html.parser")
    
    summary = []

    # Extract form inputs
    for input_tag in soup.find_all("input"):
        desc = f"Input: type={input_tag.get('type')} name={input_tag.get('name')} id={input_tag.get('id')} placeholder={input_tag.get('placeholder')}"
        summary.append(desc)

    # Extract buttons
    for button in soup.find_all("button"):
        text = button.get_text(strip=True)
        summary.append(f"Button: '{text}' id={button.get('id')}")

    # Extract important divs or elements with IDs
    for tag in soup.find_all(id=True):
        summary.append(f"Element with ID: <{tag.name}> id='{tag.get('id')}'")

    return "\n".join(summary[:30])  # limit output for prompt clarity
