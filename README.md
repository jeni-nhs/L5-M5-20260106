# Library Data Product Development

## Project Brief

The Data Engineering Library wants to improve their current quality analysis, as manually completing the task takes too much time and is less reliable. They are looking for a more efficient way to filter data using Python and automation. Management are aware of a tool called Azure DevOps and want to apply it to this process.

The main app code and processed output files are here: [python scripts](../main/python_app/)

Original sample data can be found: [sample data](../main/sample_data/)

## User stories

To make sure the project fulfils the needs of multiple members of staff and our external customers, we have written user stories to briefly describe the requirements of the project.

### Data Engineer

**As a** data engineer  
**I want to** build an automated solution that cleans and validates the library data  
**So that** I can provide stakeholders with library metrics  

**As a** data engineer  
**I want to** build a monitoring dashboard  
**So that** I can view the results of my automated pipeline  

Acceptance Criteria:
* Python scripts that transform and validate data based on rules
* Azure DevOps pipeline that runs the scripts and produces final dataset
* Monitoring dashboard for the pipeline
* Technical documentation

### Library Operations Manager

**As a** library operations manager  
**I want to** receive automated reports on my stock  
**So that** I can make informed decisions  

Acceptance Criteria:
* Dashboard with visualisations for quality metrics and trends
* Data quality issues highlighted

### Library Customers

**As a** library user  
**I want to** see my personal stats for items I have taken out on loan  
**So that** I can see an overview of my reading habits  

Acceptance Criteria:
* Dashboard with visualisations for metrics and trends

## Proposed Architecture

The proposed architecture for this project:

![architecture diagram](/assets/images/architecture_diagram.drawio.png)

The proposed architecture for the customer portal:

![customer portal](/assets/images/customer_portal.drawio.png)

## Planning

This project will require the following steps, with approximate timeframes:

### Library Metrics Dashboard

1. Explore data (1 to 2 weeks)
2. Identify and build enrichment columns (2 to 3 weeks)
   * Days borrowed
   * Other
3. Develop initial solution (12 weeks)
4. Testing (2 weeks)
5. User Acceptance Testing (2 weeks)
6. Develop finished solution (4 weeks)
7. Dashboarding (4 weeks)
8. Further UAT/development of dashboard (4 weeks)
9. Release

#### Security requirements

Staff users will need to log in using their Power BI login details.

### Customer portal

1. Requirements gathering (1 to 2 weeks)
2. Development of backend solution (12 weeks)
3. Development of frontend solution (12 weeks)
4. Dashboard development (4 weeks)

Metrics can be visualised using an open-source python solution called Streamlit, this will reduce the cost of the project.

#### Security requirements

Customers will need login details, which should be obsfucated in the backend. We will need to bring in cybersecurity consultants to ensure that this data is held securely.

## Data processing

The data will be provided in CSV format in "location".

This will be picked up as part of an automated pipeline (driven by YAML files), processed using [python scripts](../main/python_app/), and then output into a csv file.

This data will then be used as the source for a Power BI dashboard, where the semantic model will be built, and published into the Power BI service.

## Testing

Unit tests will be implemented on columns to ensure that the data is being correctly calculated. Any incorrect data will not be amended, but will be identified to allow the data to be corrected at source.

UAT testing will be required after the cleaned dataset is produced to ensure that no further columns are required. Once the dashboard is built, there will be a need for another round of UAT to ensure it is fit for purpose.

## Data Archiving

The data CSV files as provided, once processed, will be datetimestamped and archived for a set period of time. After the retention policy has expired, they will be periodically deleted.

## Dashboard

The data engineering team will need a dashboard to track the metrics of how the data processing is performing.

Key metrics that will need to be tracked include:
* Process duration
* Counts of rows that have errored (date issues, blank data, etc.)
* Count of rows of the final processed data

A mock-up of how this will look:

![dhashboard example](/assets/images/dashboard.png)

Customer facing information will include the row-level details of the errors so that they can be fixed in the source system:

![dhashboard rows_example](/assets/images/dashboard2.png)
