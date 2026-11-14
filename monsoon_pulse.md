# MONSOON PULSE

## Project concept, NASA Space Apps Challenge 2026 requirements, rules and judging criteria

[A Flood for the Century in India - NASA Science](https://images.openai.com/static-rsc-4/E1ThbUS00K-wFtWKP5twQRRnt81AG6ROTs8qTUP0JGbg1OsyNt87dur58rUYcXU_MBZTJ9v0MqayyiTvV2wehJhJi5q-YxsFtwIs-6wFKrp3GY5JxtPUIc24w9-31PJQwNDr2_1ZkwE8BlFoQUHo3VNyMztiDC5HRoSBSdbkl-k?purpose=inline)

[Southern India's Devastating Monsoon Floods Seen in Animated NASA Image | The Weather Channel](https://images.openai.com/static-rsc-4/0hLlgQnQ2cS0gPUsps5WNFws3FBFqK9DTCTetvslPd_L9RxicYi1v9LzIiwMNDh7tEgr0KAlG2w0zKCTu359nZnbwfTV2c8uLzn92TXyScoYpqBdYbOFfRWeRizv04g2VlUAMjLIxhs-gQ6DK60gAes25P6VIQHnvU461CJV9Cg?purpose=inline)

[NASA SVS | IMERG Precipitation Rates Across India's Ghats Mountains](https://images.openai.com/static-rsc-4/zQIPhqrweDX1fBgOEuLKQj_PwDsH3GeefZqoymxx41OlSvN4tExkMniSr9B4GCexS-bqBqQDsxuwXWuJ-p9_nQxXBKdpjHLcTEo_l19s5tkOH9v8fcjwQUkELf2mnwLisUu-dIiRCCXo-sinnnAMS7w6C6b1jite9RF4XW8daaQ?purpose=inline)

8

Challenge: Be An Earth System Trend Detective!\
Event: NASA Space Apps Challenge 2026\
Project: MONSOON PULSE\
Study region: Kerala, India\
Observation period: 2001–2024\
Core objective: Identify, measure, visualize and statistically evaluate long-term environmental changes using NASA Earth-observation data.

# PART 1 — Our idea

## 1. The problem

Earth's environmental systems are interconnected. Rainfall, land-surface temperature, soil moisture, vegetation and terrain all contribute to the behaviour of regional environmental systems.

These variables change over time. Their trends can differ between geographical regions, even when they are influenced by similar environmental processes.

For example:

- Rainfall extremes may increase in one district and decrease in another.
- Land-surface temperatures may rise at different rates across geographical regions.
- Soil moisture may decline while temperatures increase.
- Vegetation conditions may change alongside rainfall and soil-moisture patterns.
- Areas with different terrain characteristics may experience different levels of exposure to extreme rainfall.

Understanding these changes requires examining multiple Earth-system variables over sufficiently long observation periods and determining whether their trends are statistically significant.

This is the problem MONSOON PULSE addresses.

## 2. Our proposed solution

MONSOON PULSE is a satellite-based Earth-system trend detection and environmental intelligence platform designed to investigate long-term environmental changes across Kerala's 14 districts.

It integrates multiple NASA Earth-observation datasets, processes their historical measurements, performs statistical trend analysis and presents the results through an interactive geographical and analytical dashboard.

The platform investigates four interconnected environmental dimensions:

1. Extreme precipitation.
2. Land-surface temperature.
3. Vegetation conditions.
4. Root-zone soil moisture.

Terrain characteristics provide additional geographical context.

The objective is to identify:

- What environmental variables are changing?
- Where are those changes occurring?
- How rapidly are they changing?
- Are the observed trends statistically significant?
- How do multiple environmental variables behave together?
- Which districts show distinctive combinations of environmental changes?

The platform is designed to help researchers, students, environmental analysts and the public explore Earth-system trends through satellite data.

## 3. NASA and Earth-observation datasets

The proposed platform uses the following datasets.

[NASA Satellite Captures Amazing 3D Videos of Rain, Snow | Live Science](https://images.openai.com/static-rsc-4/g73CUQZJG4Jie0kYUtL8yMu6rkBGyUFVcEd8QdXIlRdxhKdw6h73wz8DwhvctqLSKHFZJ5QibFaQ4ffSXK_2qvjSFT4hI5U958p3xYIRLuRiXGOcDDS1Qd3fOwaXkEmsTlGdlrUaDER4FcIRNAL_G833sQI_79EMsMPVR4BXypU?purpose=inline)

NASA GPM IMERG V07

Global Precipitation Measurement

- Precipitation measurements.
- Half-hourly observations.
- Approximately 0.1° spatial resolution.
- Historical coverage beginning in 2001.

Used to investigate rainfall patterns and extreme precipitation.

[Dataset documentation](https://developers.google.com/earth-engine/datasets/catalog/NASA_GPM_L3_IMERG_V07?utm_source=chatgpt.com)

[Heatwave in Southern India - NASA Science](https://images.openai.com/static-rsc-4/Is5CwWMvwRzjxDKYwV9UQrgM8CtRzw01SkabXPgTkzoEp2Q9mFOzQKELN_uWoVaonK1ropOuHjAf12Y5YIyyTkK241v3IMhywAkwEyuSdLTu0MsuxjT-9u1z-9KKB7or0K_o5X0wYeLBUeNMo6YeVqYbPRt7jl3r8o22awLALAQ?purpose=inline)

MODIS MOD11A2 V6.1

Terra Land Surface Temperature

- Land-surface temperature.
- 8-day composites.
- Approximately 1 km resolution.

Used to examine long-term land-surface heating patterns.

[Dataset documentation](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD11A2?utm_source=chatgpt.com)

[NDVI and EVI: Vegetation Indices (MODIS) | Climate Data Guide](https://images.openai.com/static-rsc-4/vMJBBF1JTau7n8SeYIFRNtVXaXx8pzdk_tlYRSbF_NKR4kapHLpDwvM-p7GzkdIZhwlm_GdTgWFEIiADDY0mUsSDgz--YA-Nbg1eX8UwLZFqzoRUPKNU-YB14P8BAOkpoGnpY9KM4yCKkRgr0WlEj0I9uR8plIjxv-G8yzoG5JE?purpose=inline)

MODIS MOD13Q1 V6.1

Terra Vegetation Indices

- NDVI vegetation index.
- 16-day composites.
- Approximately 250 m resolution.

Used to examine changes in vegetation conditions.

[Dataset documentation](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD13Q1?utm_source=chatgpt.com)

[Soil Moisture Around the World - NASA Science](https://images.openai.com/static-rsc-4/p-MLUrSbtefezTuH0lOXhjF-eb69Kw17VLxx72scFQa7wcbI7Be3HCMSu7uyADVDtrBAf6P1s9NZHSxeYLF1wpr9CTowYio4tBgotMsU5xGXjhRH7H2XwkPUGGPhZ-rbXjP3m47-THaIzSBsNT7hTE3ndiZN4BvCPef7zIPSkyA?purpose=inline)

NASA SMAP L4 V008

Soil Moisture Active Passive

- Root-zone soil moisture.
- 3-hourly model-assimilated estimates.
- Approximately 9 km resolution.
- Available from 2015 onward.

Used to investigate changes in soil-water availability.

[Dataset documentation](https://developers.google.com/earth-engine/datasets/catalog/NASA_SMAP_SPL4SMGP_008?utm_source=chatgpt.com)

[A critical review of flood risk assessment in Kerala Post-2018: Methodological approaches, gaps, and future directions - ScienceDirect](https://images.openai.com/static-rsc-4/7_aLPeunsP_lPS5NRxagpAOc-xX3MGxFso3XNcePFY4AyLX5LRqBe-Mh0c_ERNvjRW6MuH6y2ETY0eB6t4_axGSnVy34rKfkQ8ShYwNOs8q_MleE8CePx2cmYrbi2CsQXY84b8sq-AsiVyRzVyyhoZZhQyPVsVvFVJL7DtIG_6s?purpose=inline)

NASA/USGS SRTM V003

Shuttle Radar Topography Mission

- Digital elevation model.
- Approximately 30 m resolution.
- Elevation and terrain slope.

Used to characterize geographical terrain and support rainfall-exposure analysis.

[Dataset documentation](https://developers.google.com/earth-engine/datasets/catalog/USGS_SRTMGL1_003?utm_source=chatgpt.com)

These datasets have different spatial and temporal resolutions. They are processed and aggregated appropriately for district-level analysis.

## 4. The two compound indicators

MONSOON PULSE introduces two project-defined analytical indicators.

### A. HMV — Heat–Moisture–Vegetation

HMV combines three standardized environmental variables:

- Land-surface temperature.
- Root-zone soil moisture.
- Vegetation condition (NDVI).

The proposed formula is:

\\[ HMV=\frac{Z\_{LST}-Z\_{SMAP}-Z\_{NDVI}}{3} \\]

Where:

- \\(Z\_{LST}\\) represents standardized land-surface temperature.
- \\(Z\_{SMAP}\\) represents standardized root-zone soil moisture.
- \\(Z\_{NDVI}\\) represents standardized vegetation index.

The indicator combines the three variables into one exploratory district-level composite.

It helps examine how heat, soil moisture and vegetation conditions change together over time.

A positive HMV value indicates a combination of relatively higher standardized temperature and relatively lower standardized soil moisture and vegetation values.

### B. RTE — Rainfall–Terrain Exposure

RTE combines extreme monsoon rainfall with geographical terrain characteristics.

\\[ RTE=Z\_{R95p,JJAS}\times S\_{norm} \\]

Where:

- \\(Z\_{R95p,JJAS}\\) represents standardized June–September extreme precipitation.
- \\(S\_{norm}\\) represents normalized district terrain slope.

R95p measures accumulated precipitation on days exceeding the reference-period 95th percentile of wet-day precipitation.

RTE is intended to identify districts where extreme rainfall coincides with greater terrain-slope exposure.

It is a geographical screening indicator, not a direct measurement of landslide probability or proof of landslide occurrence.

## 5. Statistical analysis

The platform examines long-term environmental changes through statistical methods.

| Method                  | Purpose                                                 |
| ----------------------- | ------------------------------------------------------- |
| Mann–Kendall test       | Detect monotonic trends                                 |
| Theil–Sen estimator     | Estimate the rate of change                             |
| Confidence intervals    | Quantify uncertainty in estimated trends                |
| Seasonal trend analysis | Examine trends while retaining calendar-month structure |
| Z-score standardization | Compare variables on standardized scales                |
| Benjamini–Hochberg FDR  | Control false discoveries across multiple tests         |
| Sensitivity analysis    | Examine how methodological choices affect results       |

The system evaluates both the direction and magnitude of trends, alongside their statistical significance.

## 6. The platform

[Climate Environment Monitoring & Assessment System :: Behance](https://images.openai.com/static-rsc-4/ypNzSjsQy-ua8WL4_LAphNRg3-9wU6FIN_SFde7zC6vzZWoTviWHkX1Z8yPT96pfQZ3qi05d5kJGg3Mx-ubkVGmuW56WI8s2V6U_gkYgdjzGZ2VP5znjUVOj_id09ZqGhOr3Z5Vne7bV3tLFhnsrH0Ud8OnhZPaab22emX1BxQU?purpose=inline)

[Exurbia Geospatial — Enterprise Satellite Intelligence](https://images.openai.com/static-rsc-4/Je8hIR6fLYc2pZAAr9uPT56LOJHCirosa6xU1E3BSNgDfpr2QalYqJbexjw4cdxwnG8IiB_CsxkPvet7gbAm2MAAjUcOxm5zHzYMfHModz8WS0PyfzMxcVXjW-j-xXdOAVyzyi-ifvf7chOBb1dU3pE58Bpn7A3X28q2eBoHW44?purpose=inline)

[Chove-Chuva montre l’évolution des dynamiques territoriales | Space for Climate Observatory](https://images.openai.com/static-rsc-4/iEpEDt0OjvXkCLfYenOZOeNeyl1vSToEq_LDc3QFtI9ZoNAHNW36IKzV7nPklo2kDywb0GVBPB2Amm82F_VTAnpyKg9KjeuPBVsoxfX9l47Xfq_gKvDBxuGjvtzhDg0_779z71KoQCwcfFXUjocQ9sB-Z39Fz-TrmzHnjWBVkkM?purpose=inline)

14

The proposed MONSOON PULSE interface includes:

- Kerala district explorer: geographical exploration of all 14 districts.
- Rainfall analysis: historical precipitation and extreme rainfall trends.
- Temperature analysis: land-surface temperature trends.
- Vegetation analysis: NDVI changes over time.
- Soil moisture analysis: root-zone soil-moisture observations.
- HMV explorer: combined heat–moisture–vegetation analysis.
- RTE explorer: rainfall–terrain exposure screening.
- Statistical analysis: trend slopes, confidence intervals, p-values and FDR-adjusted results.
- Sensitivity analysis: comparison of alternative analytical settings.

The intended experience is an interactive Earth-system investigation tool rather than a static report.

# PART 2 — NASA Space Apps Challenge 2026

## 7. Official challenge selected

Directly aligned challenge

Be An Earth System Trend Detective!

Official challenge page: [NASA Space Apps — Be An Earth System Trend Detective!](https://www.spaceappschallenge.org/2026/challenges/earth-system-trend-detective/?utm_source=chatgpt.com)

The challenge asks participants to develop a tool that can:

1. Select variables measured by Earth-science missions or produced by Earth-science models.
2. Acquire those variables for a geographical region.
3. Generate and visualize time series over a sufficiently long observation period.
4. Determine what is changing, where it is changing and how much it is changing.
5. Statistically evaluate whether the identified trends are significant.

The challenge specifically mentions methods such as t-tests, Mann–Kendall tests and confidence intervals.

It also emphasizes the value of visualizing the data alongside statistical analysis.

MONSOON PULSE addresses these objectives through multi-variable satellite data analysis, district-level time series and statistical trend evaluation.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.spaceappschallenge.org\&sz=32)

spaceappschallenge.org+1



## 8. Official 2026 event details

| Item                      | Official information             |
| ------------------------- | -------------------------------- |
| Event                     | NASA Space Apps Challenge 2026   |
| Theme                     | The Next Frontier                |
| Dates                     | November 14–15, 2026             |
| Duration                  | Two-day global hackathon         |
| Registration opened       | August 26, 2026                  |
| Full challenge statements | October 28, 2026                 |
| Submission opened         | November 14, 9:00 AM local time  |
| Submission deadline       | November 15, 11:59 PM local time |
| Team size                 | Maximum 6 participants           |
| Participation             | In-person and virtual events     |

Participants must register, select a local or virtual event and submit through their team's official Project page to be eligible for Global Judging.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.spaceappschallenge.org\&sz=32)

spaceappschallenge.org+1



# PART 3 — Official judging criteria

NASA Space Apps uses five core criteria:

1. Impact
2. Creativity
3. Validity
4. Relevance
5. Presentation

These are the official judging categories.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.spaceappschallenge.org\&sz=32)

spaceappschallenge.org+1



## 9. Impact

What judges evaluate: The potential significance of the project and the extent to which it benefits people, science or society.

For MONSOON PULSE:

- Examines environmental changes across 14 Kerala districts.
- Uses satellite observations to investigate regional Earth-system behaviour.
- Makes scientific data more accessible through an interactive platform.
- Provides a framework that could be extended to other geographical regions.
- Helps users understand long-term environmental trends.

The strongest impact argument is that the project converts complex satellite observations into geographically understandable environmental information.

## 10. Creativity

What judges evaluate: Originality and innovation in the approach.

For MONSOON PULSE:

- Combines several independent Earth-observation datasets.
- Introduces the HMV composite indicator.
- Introduces the RTE screening indicator.
- Connects environmental variables with geographical terrain characteristics.
- Integrates historical trend analysis into a single district-level exploration platform.

The originality lies in the analytical combination, regional application and integrated user experience.

## 11. Validity

What judges evaluate: Scientific credibility, technical feasibility, methodological soundness and usability.

For MONSOON PULSE:

- Uses authentic satellite and model-derived observations.
- Documents dataset sources and temporal coverage.
- Applies appropriate quality-assurance filters.
- Uses established statistical methods.
- Reports trend magnitude and statistical significance.
- Documents uncertainty and methodological limitations.
- Makes the analytical process reproducible.

This criterion depends heavily on the integrity of the actual data and calculations.

## 12. Relevance

What judges evaluate: How effectively the solution addresses the selected challenge.

For MONSOON PULSE:

| Challenge objective              | Project response                      |
| -------------------------------- | ------------------------------------- |
| Identify Earth-science variables | Five Earth-observation datasets       |
| Acquire regional data            | Kerala's 14 districts                 |
| Generate time series             | Historical 2001–2024 observations     |
| Visualize changes                | Interactive district dashboard        |
| Determine trend magnitude        | Theil–Sen slope                       |
| Test significance                | Mann–Kendall and confidence intervals |
| Investigate multiple variables   | HMV and RTE indicators                |

The project directly addresses the central requirements of the selected challenge.

## 13. Presentation

What judges evaluate: How clearly and effectively the project communicates its idea, methodology and value.

For MONSOON PULSE:

- Clear project introduction.
- Interactive demonstration.
- Readable district maps.
- Understandable time-series charts.
- Explanation of HMV and RTE.
- Statistical evidence supporting the demonstrated discovery.
- Clear explanation of NASA datasets.

A strong presentation should make the core discovery understandable within seconds.

# PART 4 — Official rules and regulations

The following summarizes the published 2026 Participant Terms and Conditions and official event instructions.

Official legal document: [2026 NASA Space Apps Participant Terms and Conditions](https://www.spaceappschallenge.org/legal/?utm_source=chatgpt.com).

## 14. Participation and registration

- Participants must register through the official NASA Space Apps website.
- Participants must select a Local Event or the Universal Event.
- Teams must have no more than six participants.
- Participants under 18 must be registered by a parent or legal guardian and accompanied by one throughout the event.
- Participation is voluntary and unpaid.
- Participants are not NASA employees or representatives simply by participating.

The legal terms also contain specific restrictions concerning participation associated with certain Chinese or Chinese-owned institutional affiliations. Those restrictions concern institutional affiliation, not Chinese nationality.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.spaceappschallenge.org\&sz=32)

spaceappschallenge.org



## 15. Project submission requirements

A submitted solution must:

- Directly address one or more official NASA Space Apps challenge statements.
- Be submitted through the official project submission process.
- Include appropriate references and resource citations.
- Contain material that the team has the legal right to publish.
- Comply with the applicable intellectual-property and licensing requirements.

NASA may publish submitted solutions on its website and make them available for others to download or use.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.spaceappschallenge.org\&sz=32)

spaceappschallenge.org



## 16. Intellectual property and open-source requirements

This is particularly important for MONSOON PULSE.

According to the official participant terms:

- Original content created for the challenge must be freely available or licensed under an OSI-compliant open-source licence.
- If no qualifying licence is specified, NASA states that it will distribute original content under Apache 2.0.
- Third-party materials must be publicly available without restriction or appropriately open-source licensed.
- Applicable third-party licences must be identified in the project documentation.
- Every source used in creating the project must be cited, including freely available and open-source resources.

Therefore, the project should provide a clear licence and attribution for its code, datasets, libraries, map resources and other third-party materials.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.spaceappschallenge.org\&sz=32)

spaceappschallenge.org



## 17. Prohibited submission content

The official terms prohibit solutions containing:

- Threatening, slanderous or obscene language.
- Personal attacks.
- Discriminatory or hateful content.
- Sexually explicit or unlawful material.
- Material promoting commercial products or services.
- Proprietary or business-sensitive information that the team has no right to publish.
- Content for which the team lacks copyright or intellectual-property rights.
- Personally identifiable information such as home addresses, personal phone numbers and sensitive identification details.

Recognizable names, voices and likenesses of persons under 18 must not be included in submissions.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.spaceappschallenge.org\&sz=32)

spaceappschallenge.org



## 18. Copyright and third-party attribution

MONSOON PULSE should provide explicit credits for:

- NASA GPM IMERG.
- NASA MODIS.
- NASA SMAP.
- NASA/USGS SRTM.
- Google Earth Engine.
- Python libraries.
- Mapping libraries.
- External geographical boundary datasets.
- Third-party visual assets.
- Any AI-generated content or externally sourced code.

Dataset citations should identify the dataset, provider, version, temporal coverage and access location.

The official terms make source attribution an important submission requirement.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.spaceappschallenge.org\&sz=32)

spaceappschallenge.org



## 19. Professional conduct and media

Participants are expected to maintain professional conduct and treat others respectfully. Harassment, bullying and discrimination are not tolerated.

The participant terms also grant NASA and the event organizers certain permissions to record and use event-related photographs, videos and submitted materials for publicity and informational purposes.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.spaceappschallenge.org\&sz=32)

spaceappschallenge.org+1



# PART 5 — Submission guidelines and practical requirements

The following separates the official requirements from the project's own recommended submission checklist.

## 20. Submission checklist

| Requirement            | MONSOON PULSE preparation                         |
| ---------------------- | ------------------------------------------------- |
| Registered participant | Confirm official registration                     |
| Selected challenge     | Be An Earth System Trend Detective                |
| Selected event         | Confirm Local or Universal Event                  |
| Team size              | Maximum 6                                         |
| Project title          | MONSOON PULSE                                     |
| Project description    | Explain problem, solution and scientific approach |
| Challenge alignment    | Explicitly address all four challenge objectives  |
| NASA data              | Identify and cite NASA datasets                   |
| Public project access  | Provide a working public project link             |
| Demonstration          | Show the platform working                         |
| References             | Cite every source and external resource           |
| Licensing              | Provide appropriate open-source licensing         |
| Submission             | Submit through official Project page              |

The official 2026 registration page specifies the submission deadline as November 15 at 11:59 PM local time.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.spaceappschallenge.org\&sz=32)

spaceappschallenge.org



## 21. Demonstration strategy

The strongest demonstration should follow a single scientific investigation.

Suggested 30-second sequence:

| Time      | Demonstration                                                          |
| --------- | ---------------------------------------------------------------------- |
| 0–5 sec   | Introduce MONSOON PULSE and its objective                              |
| 5–10 sec  | Show NASA satellite datasets                                           |
| 10–15 sec | Display Kerala and its 14 districts                                    |
| 15–21 sec | Demonstrate rainfall, temperature, vegetation and soil-moisture trends |
| 21–26 sec | Show HMV/RTE and statistical analysis                                  |
| 26–30 sec | Present one verified scientific discovery                              |

The official challenge page encourages visual time-series analysis and statistical testing. This demonstration makes those capabilities visible.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://staging-web-v2.spaceappschallenge.org\&sz=32)

staging-web-v2.spaceappschallenge.org



# PART 6 — What success looks like against the judging criteria

The following is a project-development target, not an official NASA scoring prediction.

| Criterion    | What MONSOON PULSE needs to demonstrate                                |
| ------------ | ---------------------------------------------------------------------- |
| Impact       | Meaningful regional environmental insight                              |
| Creativity   | Distinctive multi-variable analytical indicators                       |
| Validity     | Reproducible results from authentic satellite observations             |
| Relevance    | Complete implementation of the Earth-system trend-detection objectives |
| Presentation | Clear and compelling demonstration of a verified discovery             |

The strongest project is one where all five criteria reinforce one another: authentic NASA observations produce statistically defensible findings, those findings reveal a meaningful regional pattern, and the dashboard makes that pattern understandable.

# PART 7 — Final project definition

# MONSOON PULSE

## An Earth-System Trend Detection and Environmental Intelligence Platform

Challenge: Be An Earth System Trend Detective!

Mission: Investigate long-term environmental changes across Kerala using multi-sensor Earth-observation data.

Data: NASA GPM IMERG, MODIS LST, MODIS NDVI, NASA SMAP and NASA/USGS SRTM.

Analytical framework: Rainfall extremes, land-surface temperature, vegetation, soil moisture, terrain, HMV and RTE.

Statistical framework: Mann–Kendall, Theil–Sen, confidence intervals and false-discovery-rate analysis.

Interface: Interactive geographical exploration, historical time series, compound indicators and statistical reporting.

Expected outcome: A scientific exploration platform that identifies what is changing, where it is changing, how rapidly it is changing and whether the observed trends are statistically significant.

The central idea: MONSOON PULSE turns NASA Earth-observation data into an interactive investigation of Kerala's changing environmental systems.

## Official references

1. [NASA Space Apps Challenge 2026 — Official Event](https://www.spaceappschallenge.org/2026/?utm_source=chatgpt.com)
2. [Be An Earth System Trend Detective — Challenge Statement](https://www.spaceappschallenge.org/2026/challenges/earth-system-trend-detective/?utm_source=chatgpt.com)
3. [2026 Participant Terms and Conditions](https://www.spaceappschallenge.org/legal/?utm_source=chatgpt.com)
4. [About NASA Space Apps](https://www.spaceappschallenge.org/about/?utm_source=chatgpt.com)
5. [NASA's 2026 participant announcement](https://science.nasa.gov/universe/nasa-welcomes-all-ages-experience-levels-for-space-apps-challenge/?utm_source=chatgpt.com)

Important distinction: The five judging categories are official. The detailed project-specific explanations and demonstration plan above are our interpretation of how MONSOON PULSE should address them. The official challenge statement defines the scientific objectives; the HMV and RTE indicators are our own proposed analytical contributions.