# Self-Demos & OOD-Toolset

This is the official repository for [Self-Demos: Eliciting Out-of-Demonstration Generalizability in Large Language Models]().

🎉 Our paper is accepted to **NAACL 2024 Findings**.


## 📖Introduction
Current few-shot methods heavily depend on high-quality, query-specific demos, which are often lacking. When faced with *out-of-demonstration* (OOD) queries, methods that rely on hand-crafted demos or external retrievers might fail. 

**Self-Demos** is a novel prompting method that elicits the inherent generalizability in LLMs by query-aware demo generation. The generated demos strategically interpolate between existing demos and the given query, transforming the query from OOD to ID. To evaluate the effectiveness of our approach, we manually constructed **OOD-Toolset**, a dataset in the tool-using scenario with over 300 real-world APIs and 1000 instances, each consisting of three tool-use cases as demos and an OOD query.

<div align="center">
<img src=".\assets\overview.jpg" alt="Overview" width="700" />
</div>

## 🌳File Structure

```plain
Self-Demos
 ├── data
 │   ├── gsm8k
 │   │   ├── test_demos.json
 │   │   ├── test_demos_ada.json
 │   │   └── test_demos_bm25.json
 │   ├── math
 │   │   ├── test_demos.json
 │   │   ├── test_demos_ada.json
 │   │   └── test_demos_bm25.json
 │   └── tool
 │       └── test_demos.json
 ├── README.md
 ├── requirements.txt
 ├── scripts
 │   ├── ablation
 │   ├── analogical
 │   ├── few-shot
 │   ├── self-demos
 │   ├── self-icl
 │   └── zero-shot
 └── utils
     ├── evaluate.py
     ├── math.py
     └── openai.py
```

Here are some descriptions:
- `script`: contains the running and testing script for the main experiment;
- `data`: contains the dataset (raw & processed) in our experiments;
- `utils`: contains the utilities like evaluation and API invocation.

## ⚡️Quick Start

To use Self-Demos, follow these steps:

1. Clone the repository: `git clone https://github.com/hewei2001/Self-Demos.git`
2. Navigate to the project directory: `cd Self-Demos`
3. Install the required dependencies: `pip install -r requirements.txt`
3. Put your OpenAI API Keys in `./utils/raw_key.txt`
3. Run the script in `./scripts/self-demos/`


## ✨OOD-Toolset
**Construction Process**:

1. Data Collection: The raw data was derived from a tool-use corpus created by [ToolAlpaca](https://github.com/tangqiaoyu/ToolAlpaca), which included a wide range of real-world APIs with descriptions, usage specifications, and multiple simulated tool use cases.
2. Rule-based Cleaning: The raw data was structured and filtered based on specific rules to enhance relevance and quality, removing entries with missing function descriptions, non-JSON format, and excessive complexity.
3. Manual Data Cleaning: Human annotators refined the corpus to ensure clarity in queries, correct logical structure, and consistency in parameter values.
4. Query and Demonstration Construction: After cleaning, we proceeded to select instances from the tool-use cases and construct corresponding demonstrations.

For more details, you can check out the Appedix B of our [paper]().

**Example of Cleaned Dataset**:

<div align="center">
<img src=".\assets\cleaned_dataset.jpg" alt="Example of Cleaned Dataset" width="600" />
</div>
The cleaned dataset is structured into four parts for each API:
- API Name: The identifier for the tool.
- Description: A brief overview of the tool's purpose.
- Usage Specifications: Detailed information on API calls and parameter interfaces.
- Tool-use Cases: Simulated use cases demonstrating the tool's application.

**Example of Instance in OOD-Toolset**:

<div align="center">
<img src=".\assets\instance.jpg" alt="Example of Instance in OOD-Toolset" width="600" />
</div>

For each test instance, we provided three cases from the same API as initial available few-shot demos (also referred to as *seed demos*). Notably, in the OOD setting, the sub-APIs in seed demos differ from those needed in the final query.

For example, the function required for the Query is <u>ROUTE</u>. Consequently, tool-use cases related to this sub-API should not be included in the seed demos.

## 📈Case Study

We have picked up 3 representative cases for further analysis:

**① Self-Demos succeeded and Few-shot / Self-ICL failed.**

> API Name: Privacy.com
>
> Query: I'm planning to shop at Amazon for some electronics, but I don't want to use my main credit card. Can you create a new card specifically for Amazon with a **spending limit of $500** and provide me with the card details?
>
> Function should be called: `createNewCard`
>
> - Create a new card for a specific merchant
> - Parameters: {"merchantName": "Required. string. The name of the merchant for which the card is being created.", "spendingLimit": "integer. **The spending limit for the card in cents**."}
>
> Right Answer (Self-Demos): `createNewCard(merchantName='Amazon', spendingLimit=50000)`
>
> Wrong Answer (Few-shot & Self-ICL + FS): `createNewCard(merchantName='Amazon', spendingLimit=500)`

Explanation: In this case, Self-Demos **successfully captures that the unit** of the `spendingLimit` parameter is in cents, thanks to its generated relevant demos. However, **Few-shot and Self-ICL fail in this regard due to either the absence of relevant demos or the generation of irrelevant ones**.

**② Few-shot succeeded and Self-Demos failed.**

> API Name: Open Data Minneapolis
>
> Query: Retrieve the schedule for the 'Route 5' bus in Minneapolis.
>
> Function should be called: `getTransportationData`
>
> - Retrieve transportation data such as **public transit schedules**, bike lanes, and parking regulations.
> - Parameters: {"transportationType": "Required. string. Type of transportation data to filter results."}
>
> Right Answer (Few-shot): `getTransportationData(transportationType='bus')`
>
> Wrong Answer (Self-Demos): `getTransportationData(transportationType='public transit schedules')`

Explanation: In this case, **Self-Demos was misled by some expressions in the usage specification**, thereby affecting the final prediction. On the other hand, **Few-shot, benefiting from its lack of comprehensive consideration, occasionally achieves correctness**.

**③ Both failed.**

> API Name: KKBOX
>
> Query: I'm looking for a specific track **by Ed Sheeran**. Can you help me find it on KKBOX?
>
> Function should be called: `tracksSearch`
>
> - Search for specific tracks by their **name, artist, or album**.
> - Parameters: {"q": "Required. string. The search query for tracks.", "type": "string. **One of: [track, artist, album]. The type of search to perform**."}
>
> Right Answer: `tracksSearch(q='Ed Sheeran', type='artist')`
>
> Wrong Answer (Both methods): `tracksSearch(q='Ed Sheeran', type='track')`

Explanation: This is an interesting case where all methods, even with GPT-4 models, incorrectly set `type` to 'track' instead of the specific artist. We speculate that this is **due to the hallucination within the model**.

## 🔎Citation

If you find Self-Demos useful or relevant to your project and research, please kindly cite our paper:

```Plain
@article{
    TODO
}
```
