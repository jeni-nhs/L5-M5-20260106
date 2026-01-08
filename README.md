# Library Data Product Development

## Project Brief

A library wants to improve their current quality analysis, as manually completing the task takes too much time and is less reliable. They are looking for a more efficient way to filter data using Python and automation. They have heard of a tool called Azure DevOps. and want to apply it to their process.

## Proposed Architecture

The proposed architecture for this project:

![architecture diagram](/assets/images/architecture_diagram.drawio.png)

The proposed architecture for the customer portal:

![customer portal](/customer_portal.drawio.png)

## User stories

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

## Planning

1. Explore data
2. Add additional columns:
   * Days borrowed
   * Other
3. Tests
4. UAT
5. Dashboarding
6. Further UAT
7. Release

## Data processing

The data will be provided in CSV format in <location>.

This will be picked up as part of a pipeline, processed using python, and then output into a csv file or database.

This data will then be used as the source for a Power BI dashboard, where the semantic model will be built, and published into the Power BI service.

## Testing

Unit tests will be implemented on columns to ensure that the data is being correctly calculated, this includes the number of days a book was borrowed for, this will mean that we can then do testing on the data quality to easily find dates that are incorrect (returned before checkout), or identify if they have possibly been input incorrectly (wildly out of range borrowed days).

UAT testing will be required after the cleaned dataset is produced to ensure that no further columns are required. Once the dashboard is built, there will be a need for another round of UAT to ensure it is fit for purpose.
