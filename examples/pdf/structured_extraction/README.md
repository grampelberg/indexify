# Structured Extraction from PDFs with GPT-4

In this cookbook, we'll explore how to create a PDF schema extraction pipeline using Indexify, the Marker PDF extractor, and OpenAI's language models. By the end of the document, you should have a pipeline capable of ingesting PDF documents and extracting structured information based on a predefined schema.

![Preview data](https://i.postimg.cc/XYCqNP0p/hoa.png)

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Setup](#setup)
   - [Install Indexify](#install-indexify)
   - [Install Required Extractors](#install-required-extractors)
4. [Creating the Extraction Graph](#creating-the-extraction-graph)
5. [Implementing the Schema Extraction Pipeline](#implementing-the-schema-extraction-pipeline)
6. [Running the Schema Extraction](#running-the-schema-extraction)
7. [Customization and Advanced Usage](#customization-and-advanced-usage)
8. [Conclusion](#conclusion)

## Introduction

The schema extraction pipeline will consist of two steps:
- PDF to Text extraction using the pre-built extractor `tensorlake/marker`.
- Schema-based information extraction using `tensorlake/schema` with OpenAI's language models.

## Prerequisites

Before we begin, ensure you have the following:

- Create a virtual env with Python 3.9 or later
  ```shell
  python3.9 -m venv ve
  source ve/bin/activate
  ```
- `pip` (Python package manager)
- An OpenAI API key
- Basic familiarity with Python and command-line interfaces

## Setup

### Install Indexify

First, let's install Indexify using the official installation script & start the server:

```bash
curl https://getindexify.ai | sh
./indexify server -d
```
This starts a long-running server that exposes ingestion and retrieval APIs to applications.

### Install Required Extractors

Next, we'll install the necessary extractors in a new terminal:

```bash
pip install indexify-extractor-sdk
indexify-extractor download tensorlake/marker
indexify-extractor download tensorlake/schema
```

Once the extractors are downloaded, you can start them:
```bash
indexify-extractor join-server
```

## Creating the Extraction Graph

The extraction graph defines the flow of data through our schema extraction pipeline. We'll create a graph that first extracts text from PDFs using Marker, then sends that text to the schema extractor for structured information extraction.

Create a new Python file called `pdf_schema_extraction_graph.py` and add the following code:

```python
from indexify import IndexifyClient, ExtractionGraph
from pydantic import BaseModel

class Invoice(BaseModel):
    invoice_number: str
    date: str
    account_number: str
    owner: str
    address: str
    last_month_balance: str
    current_amount_due: str
    registration_key: str
    due_date: str

schema = Invoice.model_json_schema()

client = IndexifyClient()

extraction_graph_spec = f"""
name: 'pdf_schema_extractor'
extraction_policies:
  - extractor: 'tensorlake/marker'
    name: 'pdf_to_text'
  - extractor: 'tensorlake/schema'
    name: 'text_to_schema'
    input_params:
      service: 'openai'
      model_name: 'gpt-3.5-turbo'
      key: 'YOUR_OPENAI_API_KEY'
      schema_config: {schema}
      additional_messages: 'Extract information in JSON according to this schema and return only the output.'
    content_source: 'pdf_to_text'
"""

extraction_graph = ExtractionGraph.from_yaml(extraction_graph_spec)
client.create_extraction_graph(extraction_graph)
```

Replace `'YOUR_OPENAI_API_KEY'` with your actual OpenAI API key.

You can run this script to set up the pipeline:
```bash
python pdf_schema_extraction_graph.py
```

## Ingestion and Retreival from Schema Extraction Pipeline

Now that we have our extraction graph set up, we can upload files and make the pipeline extract structured information:

Create a file `upload_and_retreive.py`:

```python
import os
import requests
from indexify import IndexifyClient
import json

def download_pdf(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as f:
        f.write(response.content)
    print(f"PDF downloaded and saved to {save_path}")

def extract_schema_from_pdf(pdf_path):
    client = IndexifyClient()
    
    # Upload the PDF file
    content_id = client.upload_file("pdf_schema_extractor", pdf_path)
    
    # Wait for the extraction to complete
    client.wait_for_extraction(content_id)
    
    # Retrieve the extracted content
    extracted_data = client.get_extracted_content(
        content_id=content_id,
        graph_name="pdf_schema_extractor",
        policy_name="text_to_schema"
    )
    
    return json.loads(extracted_data[0]['content'].decode('utf-8'))

# Example usage
if __name__ == "__main__":
    pdf_url = "https://pub-226479de18b2493f96b64c6674705dd8.r2.dev/Statement_HOA.pdf"
    pdf_path = "sample_invoice.pdf"
    
    # Download the PDF
    download_pdf(pdf_url, pdf_path)
    
    # Extract schema-based information from the PDF
    extracted_info = extract_schema_from_pdf(pdf_path)
    print("Extracted information from the PDF:")
    print(json.dumps(extracted_info, indent=2))
```

You can run the Python script to extract schema-based information from PDF files:
```bash
python upload_and_retreive.py
```
<img src="https://docs.getindexify.ai/example_code/pdf/structured_extraction/carbon.png" width="600"/>

## Customization and Advanced Usage

You can customize the schema extraction process by modifying the `Invoice` class and the `additional_messages` in the extraction graph. For example:

- To focus on specific fields:
  ```python
  additional_messages: 'Extract only the invoice_number, date, and current_amount_due from the text.'
  ```

- To handle multiple invoice formats:
  ```python
  additional_messages: 'This text may contain information from various invoice formats. Extract as much information as possible according to the schema.'
  ```

You can also experiment with different OpenAI models by changing the `model_name` parameter to find the best balance between speed and accuracy for your specific use case.

## Conclusion

This example demonstrates the power of using Indexify for schema-based PDF extraction:

1. **Scalability**: Indexify server can process numerous PDFs uploaded into it, automatically retrying failed steps on another machine if necessary.
2. **Flexibility**: You can easily swap out the PDF extraction model or the schema extraction service to suit your specific needs.
3. **Structured Data Extraction**: By using a predefined schema, you ensure that the extracted information is consistently formatted and ready for further processing or analysis.

## Next Steps

- Explore more about Indexify in our documentation: https://docs.getindexify.ai
- Learn how to use Indexify for other document processing tasks, such as [entity extraction from PDF documents](https://github.com/tensorlakeai/indexify/blob/main/docs/docs/examples/mistral/pdf-entity-extraction-cookbook.md)