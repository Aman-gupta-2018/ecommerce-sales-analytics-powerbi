# Power BI Dashboard Build Guide — Complete Beginner Tutorial

> You are NEW to Power BI. This guide assumes you know **nothing** about Power BI.
> Every step is written like a recipe: open this, click that, type this.
> Go slowly, follow it in order, and you will end up with a professional 4-page dashboard.
> **Total time: about 2–3 hours.**

---

## TABLE OF CONTENTS
- [Part 0 — What you are building & concepts you must know](#part-0)
- [Part 1 — Install Power BI Desktop](#part-1)
- [Part 2 — Import your data](#part-2)
- [Part 3 — Check & fix data types](#part-3)
- [Part 4 — Build relationships (the "star schema")](#part-4)
- [Part 5 — Mark the Date table](#part-5)
- [Part 6 — Create calculated columns](#part-6)
- [Part 7 — Create DAX measures](#part-7)
- [Part 8 — Build Page 1: Executive Overview](#part-8)
- [Part 9 — Build Page 2: Profitability Deep-Dive](#part-9)
- [Part 10 — Build Page 3: Customer RFM](#part-10)
- [Part 11 — Build Page 4: Operations](#part-11)
- [Part 12 — Add navigation buttons & bookmarks](#part-12)
- [Part 13 — Save, Publish & share](#part-13)
- [Part 14 — Troubleshooting common errors](#part-14)
- [Part 15 — Glossary of Power BI words](#part-15)

---

<a name="part-0"></a>
## PART 0 — WHAT YOU ARE BUILDING & CONCEPTS YOU MUST KNOW

### The big picture
A dashboard is a page (or several pages) full of **charts and numbers**. When a user clicks a chart or filter, everything updates automatically. You will build 4 pages:

| Page | What it shows |
|------|----------------|
| Page 1 — Executive Overview | Total revenue, profit, orders, customers + trends by month, category, region |
| Page 2 — Profitability | The "money story" — how discounts destroy profit |
| Page 3 — Customer Segmentation | Which customers are most valuable (RFM model) |
| Page 4 — Operations | Shipping speed, weekdays, order volume |

### The 5 most important ideas in Power BI

**Idea 1 — Tables in your data are called "tables" or "models".**
Power BI is NOT Excel. Excel has one grid. Power BI has many tables, and you connect them so they talk to each other.

**Idea 2 — Fact tables vs Dimension tables.**
- A **Fact table** = things that happen, over and over. Your `fact_orders` table has one row per order line. It contains numbers (Sales, Profit, Quantity).
- A **Dimension table** = descriptions you slice by. `dim_customers` describes who bought. `dim_products` describes what was sold. `dim_date` is a calendar. `dim_geography` describes where.

You connect a fact table to dimension tables using matching columns called **keys** (like `Customer ID`). This layout (one fact in the middle, dimensions around it) is called a **star schema**. Professional analysts use it because it is fast and correct.

**Idea 3 — Measures vs Calculated columns.**
- A **Measure** is a formula you write in DAX (Power BI's language) that calculates a NUMBER, and it changes depending on what is selected on the page. Example: `Total Revenue = SUM(fact_orders[Sales])`. It shows $2,297,201 for everything, or just $500,000 if you select one category. **Measures are the most important thing you will make.**
- A **Calculated column** is a formula that adds a NEW column to a table, computed once per row. Example: a "Discount Band" column that says "No Discount" / "1-10%" / "20%+".

**Idea 4 — DAX is the formula language.**
You don't need to memorize it. You will copy-paste formulas from this guide. Just understand the pattern:
```
Measure Name = CALCULATION(Table[Column], extra filters)
```
`SUM`, `AVERAGE`, `DISTINCTCOUNT`, `CALCULATE`, `DIVIDE` are the ones you'll use most.

**Idea 5 — Views.**
On the left edge of Power BI there are **3 icons** (like little tabs). Click them to switch views:
- **Report** view (top icon, a chart/paper shape) — where you design pages and visuals.
- **Data** view (middle icon, a table shape) — where you see raw tables and add calculated columns.
- **Model** view (bottom icon, three connected squares) — where you build relationships.

Every time I say "go to Report view / Data view / Model view", click the matching icon on the far-left vertical bar.

---

<a name="part-1"></a>
## PART 1 — INSTALL POWER BI DESKTOP

1. Open your web browser.
2. Go to: **https://powerbi.microsoft.com/desktop/**
3. Click the **Download** button.
4. A file like `PBIDesktopSetup_xxx.exe` downloads. Double-click it.
5. Click **Next → Next → Install** (accept all defaults).
6. When it finishes, check **Launch Power BI Desktop** and click **Finish**.
7. Power BI opens with a start screen. Click **Get started** (a blank report opens).
8. If it asks you to **Sign in** — you can skip it for now (there is an "X" or "Not now" option). You only need to sign in later for publishing.

> You now have a blank canvas. We will fill it in the next steps.

---

<a name="part-2"></a>
## PART 2 — IMPORT YOUR DATA

Your cleaned data files are already created in the folder:
```
C:\Users\ASUS\OneDrive\Desktop\Data Analyst\data\cleaned\
```

You will import **7 files**. Do this one file at a time. It takes practice but is simple.

### 2.1 Import `fact_orders.csv` (the big one)

1. In Power BI, look at the top ribbon (the menu bar). Click the **Home** tab (it's already selected).
2. Click the **Get data** button (left side). A small dropdown opens.
3. Choose **Text/CSV**. A file-picker window opens.
4. Navigate to `data\cleaned`, select **fact_orders.csv**, and click **Open**.
5. A preview window opens showing a sample of your data.
   - Check the bottom: it says "Number of columns: 26".
   - Look for a checkbox near the top: **"The first row contains column headers"**. Make sure it is CHECKED (Power BI usually checks it automatically).
6. Click **Load** (bottom-right).
7. Wait a few seconds — Power BI is importing 9,994 rows.

You are back on the report canvas. **Do NOT worry** that you see nothing yet. The table is inside Power BI now.

### 2.2 Import the remaining 6 files

Repeat the exact same steps (Get data → Text/CSV → select file → Load) for:

| File | What it is |
|------|-----------|
| `dim_customers.csv` | Customer descriptions |
| `dim_products.csv` | Product descriptions |
| `dim_geography.csv` | City / State / Region descriptions |
| `dim_date.csv` | Calendar of every day from 2014–2017 |
| `dim_shipmode.csv` | 4 shipping methods |
| `customer_rfm_analysis.csv` | One row per customer with RFM scores |

### 2.3 Check that all tables loaded

1. On the RIGHT side of the screen you see the **Fields** pane (a panel listing things).
2. It shows a list of your tables: `fact_orders`, `dim_customers`, `dim_products`, `dim_geography`, `dim_date`, `dim_shipmode`, `customer_rfm_analysis`.
3. If any is missing, repeat step 2.2 for it.

> **If the Fields pane is not visible:** click the **View** tab in the ribbon, then tick the **Fields** checkbox.

---

<a name="part-3"></a>
## PART 3 — CHECK & FIX DATA TYPES

Power BI guessed the type of every column when it imported. Dates might have been read as text, and that breaks time analysis. Let's fix them.

### 3.1 Check the fact table columns

1. In the **Fields** pane, find `fact_orders`.
2. Click the little arrow (chevron) next to `fact_orders` to expand it.
3. Look at the icons next to each column:
   - Calendar icon = Date type ✅ (we need this for `Order Date` and `Ship Date`)
   - "123" icon = number ✅ (we need this for `Sales`, `Profit`, `Quantity`, `Discount`)
   - "ABC" icon = text

If `Order Date` or `Ship Date` show an "ABC" icon, do the following:

### 3.2 Fix a date column (only if needed)

1. Click the **Transform Data** button on the Home ribbon. This opens **Power Query Editor** (a separate window). This is normal.
2. On the right, in the **Queries** panel, click `fact_orders`.
3. Find the column `Order Date`. Right-click the column header.
4. Choose **Change Type → Date**.
5. Do the same for `Ship Date` → **Date**.
6. Click **Close & Apply** (top-left) to go back to the report.
7. In the Fields pane, the calendar icon should now appear.

### 3.3 Check the date table

1. Expand `dim_date` in the Fields pane.
2. Check `dim_date[Date]` has a calendar icon. If not, fix it using the same Power Query steps (column name is `Date` → change type to **Date**).

> **Why this matters:** Time-intelligence DAX functions (monthly trends, YoY) only work when dates are actually Date type.

### 3.4 FIX: Columns show as "Column1", "Column2", "Column3" (very common!)

If any table shows columns named **Column1 / Column2 / Column3**, it means Power BI imported the file WITHOUT using the first row as the header — the real column names (`Customer ID`, `Customer Name`, etc.) got treated as a regular data row.

**Example:** your `dim_customers` table shows `Column1`, `Column2`, `Column3` instead of `Customer ID`, `Customer Name`, `Segment`.

**Fix it in 3 clicks:**

1. Click **Transform Data** on the Home ribbon. Power Query Editor opens.
2. In the **Queries** panel on the left, click the table with the problem (e.g. `dim_customers`).
3. On the **Transform** tab of the ribbon, click **Use First Row as Headers**.

   > The columns instantly rename to `Customer ID`, `Customer Name`, `Segment`.

4. **Check for a bad data row:** because the header row was previously read as data, your first data row is now wrong (it contains the words "Customer ID", "Customer Name", "Segment"). Look at the first row:
   - If Row 1 contains those words, right-click the row number → **Delete Rows** → check it's selected → **OK**.
5. Repeat steps 1–4 for **every** table that has Column1/2/3 names.
6. Click **Close & Apply**.

**Check all 7 tables after fixing:**
- `fact_orders` should have columns like `Order ID`, `Sales`, `Profit` (NOT `Column26`).
- `dim_customers` → `Customer ID`, `Customer Name`, `Segment`.
- `dim_products` → `Product ID`, `Product Name`, `Category`, `Sub-Category`.
- `dim_geography` → `Geo ID`, `City`, `State`, `Region`, ...
- `dim_date` → `Date`, `Year`, `Month`, ...
- `dim_shipmode` → `Ship Mode ID`, `Ship Mode`.
- `customer_rfm_analysis` → `Customer ID`, `Monetary`, `Customer Segment`, ...

> **Prevention for future imports:** when the preview window appears during **Get Data → Text/CSV**, always confirm the checkbox **"The first row contains column headers"** is ticked **before** clicking Load. If it's already ticked, the columns come in correctly the first time.

---

<a name="part-4"></a>
## PART 4 — BUILD RELATIONSHIPS (THE "STAR SCHEMA")

This is where your data starts talking to each other. Power BI will auto-detect some relationships, but we'll build them properly and deliberately.

### 4.1 Go to Model view

1. Click the **Model** icon on the far-left vertical bar (the bottom icon, looks like 3 connected boxes).
2. You now see your tables as boxes, with lines (relationships) between some of them.
3. Power BI may have created relationships automatically. We are going to make sure ALL of these exist:

| From table & column | To table & column | Direction |
|---------------------|-------------------|-----------|
| `dim_customers[Customer ID]` | `fact_orders[Customer ID]` | One to many |
| `dim_products[Product ID]` | `fact_orders[Product ID]` | One to many |
| `dim_geography[Geo ID]` | `fact_orders[Geo ID]` | One to many |
| `dim_date[Date]` | `fact_orders[Order Date]` | One to many |
| `dim_customers[Customer ID]` | `customer_rfm_analysis[Customer ID]` | One to one |

### 4.2 Create a relationship by dragging

The easiest way:
1. In Model view, look for the `dim_date` box.
2. **Left-click and HOLD** the `Date` field inside `dim_date`.
3. **Drag** it onto the `Order Date` field inside `fact_orders`, then release.
4. A window **Create relationship** opens.
   - **Table 1 (1):** `dim_date` / `Date`
   - **Table 2 (Many):** `fact_orders` / `Order Date`
   - Click **OK**.
5. A line now connects them.

Repeat the drag-and-drop for the other 4 relationships listed above.

### 4.3 Turn off cross-filtering in one direction (professional touch)

1. In Model view, click the line between `dim_date` and `fact_orders`.
2. The **Properties** pane appears on the right.
3. Find **Cross filter direction**. Click the dropdown and set it to **Single**.
4. Do the same for every relationship (set direction to **Single**).

### 4.4 What about `dim_shipmode`?

The `dim_shipmode` table has an ID that does NOT match the text in `fact_orders[Ship Mode]`, so we will NOT link it. We will use `fact_orders[Ship Mode]` directly on the Operations page. (It is a tiny table; you can ignore it or delete it by right-clicking it in the Fields pane → Delete.)

### 4.5 Check your star schema looks right

You should see `fact_orders` in the middle with lines going out to `dim_customers`, `dim_products`, `dim_geography`, and `dim_date` — like a star.

> **Test it now (important):**
> 1. Click the **Report** icon (top-left).
> 2. In the Fields pane, expand `dim_products` and tick the checkbox next to `Category`.
> 3. Expand `fact_orders` and tick `Sales`.
> 4. A chart appears automatically. Click one of the bars — the whole page filters.
> 5. Right-click the chart → **Delete** to remove this test chart.
> If clicking a bar didn't filter anything, your relationships are missing. Go back to 4.2.

---

<a name="part-5"></a>
## PART 5 — MARK THE DATE TABLE

This tells Power BI "this is the master calendar", which activates fancy date functions.

1. Go to **Model view**.
2. In the **Fields** pane (right side), find `dim_date`. Click it.
3. With `dim_date` selected, find the **Properties** pane. There is a dropdown labeled **Mark as date table**.
4. Change it from "No" to **Mark as date table**.
5. A dialog asks which column to use. Choose **Date** (it should already be selected).
6. Click **OK**.

> Now when you use date fields, Power BI gives you a built-in hierarchy: Year → Quarter → Month → Day. We'll use this later.

---

<a name="part-6"></a>
## PART 6 — CREATE CALCULATED COLUMNS

We need ONE calculated column: **Discount Band** (so we can chart "No Discount vs 1-10% vs 20%+").

### 6.1 What's the difference again?
- Calculated column = new COLUMN in a table (one value per row).
- Measure = new NUMBER that changes with filters.

### 6.2 Create the "Discount Band" column

> **⚠️ READ THIS FIRST — the most common beginner mistake:**
> This must be created as a **CALCULATED COLUMN**, NOT a measure.
> - A calculated column sees each row ONE AT A TIME, so `fact_orders[Discount] = 0` gives a clear Yes/No per row. ✅
> - A measure sees the WHOLE column at once (9,994 values), so it fails with:
>   *"A single value for column 'Discount' in table 'fact_orders' cannot be determined. This can happen when a measure or function formula refers to a column that contains many values without specifying an aggregation..."*
>
> **If you saw that error**, you accidentally created a measure. Fix it now:

**Step A — delete the wrongly-created "Discount Band":**
1. Click the **Report** icon (top-left).
2. In the **Fields** pane (right side), find `Discount Band` under `fact_orders`.
3. Right-click it → **Delete**. Confirm.
   - If it doesn't appear under `fact_orders`, look for it in any table/measures folder you created — delete it there too.

**Step B — create it correctly as a CALCULATED COLUMN:**
1. Click the **Data** icon (middle icon, table shape) on the far-left bar.
2. In the **Fields** pane (right), click `fact_orders` (this shows the table as a grid).
3. Look at the top ribbon. There should be a **"Table tools"** tab. Click it.
4. Click the **New column** button (NOT "New measure"). ✅
   - How to tell them apart: **New column** is on the **Table tools** ribbon in **Data view**. "New measure" is usually a right-click option or on the Home/Modeling ribbon. If you don't see "Table tools", you are in the wrong view — go back to step 1.
5. A formula bar appears near the top of the screen. Replace the default text with EXACTLY this:

```
Discount Band =
SWITCH(
    TRUE(),
    fact_orders[Discount] = 0, "No Discount",
    fact_orders[Discount] <= 0.10, "1-10%",
    fact_orders[Discount] <= 0.20, "11-20%",
    fact_orders[Discount] <= 0.30, "21-30%",
    "30%+"
)
```

6. Click the **checkmark (✓)** on the left side of the formula bar (or press **Enter**).
7. Scroll to the far right of the grid — a new column `Discount Band` now appears **as a column in the grid**.

**Step C — verify it's a column, not a measure:**
- You can see `Discount Band` as an actual column in the Data view grid (a measure never appears there). ✅
- If instead the error returns or nothing appears as a column, repeat Step A + Step B carefully.

> **How to read the formula:** SWITCH checks conditions top to bottom. If Discount is 0 → "No Discount". If it's 10% or less → "1-10%". If 20% or less → "11-20%", and so on. The last "30%+" is the fallback for anything bigger.

> **Rule of thumb for the whole project:**
> - Use **New column** when the formula must look at ONE ROW's data to make a NEW column (like Discount Band).
> - Use **New measure** when the formula aggregates/sums many rows into ONE number (like `Total Revenue = SUM(...)`).

---

<a name="part-7"></a>
## PART 7 — CREATE DAX MEASURES

Now the fun (and impressive) part. You'll paste 30+ measures. Take your time.

### 7.1 How to create a measure (learn this once)

1. Click the **Report** icon (top-left).
2. In the **Fields** pane, **right-click** the `fact_orders` table.
3. Choose **New measure**.
4. A formula bar appears at the top. Type or paste the measure, then press **Enter**.
5. The measure appears in the Fields pane under `fact_orders` with a calculator icon (Σ).

### 7.2 Optional but tidy: make a "Measures" folder

1. On the **Home** ribbon, click **Enter data**.
2. Leave the table blank, rename it to **Measures** in the "Name" box at the top.
3. Click **Load**.
4. Now right-click the `Measures` table → **New measure** and create ALL measures there instead. The measures still work — they just live in a tidy folder. (If this confuses you, skip it and create measures under `fact_orders`.)

### 7.3 Paste the measures

> **⚠️ THE #1 CAUSE OF "syntax is incorrect" ERRORS — READ THIS FIRST:**
> The formula bar accepts **ONLY ONE measure at a time**. 
> **NEVER** copy the whole group (all the measures together) and paste them at once. Power BI will try to read the entire block as ONE formula and fail with `The syntax for 'Total' is incorrect.` (or similar).
>
> **The correct rhythm — repeat these 3 steps for EVERY measure:**
> 1. Right-click a table → **New measure**.
> 2. Paste **exactly ONE block** (a single measure, like just `Total Revenue = SUM(fact_orders[Sales])`).
> 3. Click the **✓** or press **Enter**.
>
> That's it. One paste = one measure. Then start the next one.

**Step-by-step for Group A (9 measures — do them one by one):**

1. In the **Fields** pane, right-click `fact_orders` → **New measure**.
2. Paste **only this line**, then Enter:
   ```
   Total Revenue = SUM(fact_orders[Sales])
   ```
3. Right-click `fact_orders` → **New measure** again. Paste **only this line**, then Enter:
   ```
   Total Profit = SUM(fact_orders[Profit])
   ```
4. Keep going, **one paste each**, for:
   ```
   Total Orders = DISTINCTCOUNT(fact_orders[Order ID])
   ```
   ```
   Total Customers = DISTINCTCOUNT(fact_orders[Customer ID])
   ```
   ```
   Total Quantity = SUM(fact_orders[Quantity])
   ```
   ```
   Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0)
   ```
   ```
   Avg Order Value = DIVIDE([Total Revenue], [Total Orders], 0)
   ```
   ```
   Avg Discount = AVERAGE(fact_orders[Discount])
   ```
   ```
   Avg Shipping Days = AVERAGE(fact_orders[Shipping Days])
   ```

> **Recovering from the "syntax is incorrect" error right now:**
> 1. The formula bar still shows the pasted mess. Press **Escape (Esc)** or click the **X** to cancel — do NOT press Enter or the ✓.
> 2. Check the **Fields** pane: if Power BI created a broken measure (something like a weird partial name or "Error"), right-click it → **Delete**.
> 3. Now start over with the rhythm above: one paste per measure.

> **How to read these formulas:**
> - `SUM(fact_orders[Sales])` = add up all the Sales numbers.
> - `DISTINCTCOUNT(fact_orders[Order ID])` = count unique Order IDs (one order can appear on several lines).
> - `DIVIDE([Total Profit], [Total Revenue], 0)` = profit divided by revenue; the `0` is a safety net (returns 0 instead of an error if divided by zero).
> - A measure can call other measures: `Profit Margin %` uses `[Total Profit]` and `[Total Revenue]` (bracket = another measure).

**Group B — Time intelligence (YoY / MoM):**

> **Remember the rule:** the blocks below contain MANY measures. Still paste them **one at a time** — right-click a table → New measure → paste ONE measure → Enter. Repeat.

```dax
Revenue PY = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(dim_date[Date]))

Revenue YoY Change = [Total Revenue] - [Revenue PY]

Revenue YoY Growth % = DIVIDE([Revenue YoY Change], [Revenue PY], 0)

Revenue MTD = TOTALMTD([Total Revenue], dim_date[Date])

Revenue PM = CALCULATE([Total Revenue], PREVIOUSMONTH(dim_date[Date]))

Revenue MoM Growth % = DIVIDE([Total Revenue] - [Revenue PM], [Revenue PM], 0)

Profit Margin YoY pp = [Profit Margin %] - CALCULATE([Profit Margin %], SAMEPERIODLASTYEAR(dim_date[Date]))

Revenue YTD = TOTALYTD([Total Revenue], dim_date[Date])
```

**Group C — Discount & profitability (the money story):**

```dax
Discounted Revenue = CALCULATE([Total Revenue], fact_orders[Has Discount] = 1)

Full Price Revenue = CALCULATE([Total Revenue], fact_orders[Has Discount] = 0)

Loss Orders = CALCULATE([Total Orders], fact_orders[Is Profitable] = 0)

Loss Rate % = DIVIDE([Loss Orders], [Total Orders], 0)

Discounted Margin % = CALCULATE([Profit Margin %], fact_orders[Has Discount] = 1)

Full Price Margin % = CALCULATE([Profit Margin %], fact_orders[Has Discount] = 0)

Potential Profit Recovery =
CALCULATE(SUM(fact_orders[Profit]), fact_orders[Discount] > 0.2, fact_orders[Profit] < 0)
```

**Group D — Products & categories:**

```dax
Category Revenue Share =
DIVIDE([Total Revenue], CALCULATE([Total Revenue], ALLSELECTED(dim_products[Category])), 0)

Losing Products = CALCULATE(COUNTROWS(dim_products), fact_orders[Is Profitable] = 0)

Top 5 Products Revenue = CALCULATE([Total Revenue], TOPN(5, ALL(dim_products), [Total Revenue]))
```

**Group E — Customers & RFM:**

```dax
Customers in Segment = COUNTROWS(dim_customers)

Segment Revenue = SUM(customer_rfm_analysis[Monetary])

Avg Customer LTV = AVERAGE(customer_rfm_analysis[Monetary])

Champions Count = CALCULATE(COUNTROWS(customer_rfm_analysis), customer_rfm_analysis[Customer Segment] = "Champions")

Repeat Customers =
CALCULATE([Total Customers],
    FILTER(VALUES(fact_orders[Customer ID]),
        CALCULATE(DISTINCTCOUNT(fact_orders[Order ID])) >= 2))

Repeat Purchase Rate % = DIVIDE([Repeat Customers], [Total Customers], 0)
```

**Group F — Operations:**

```dax
Late Order Rate % =
DIVIDE(
    CALCULATE(COUNTROWS(fact_orders), fact_orders[Shipping Days] > 5),
    COUNTROWS(fact_orders), 0)
```

**Group G — Dynamic title (for polish):**

```dax
Dynamic Title = "Sales Performance " & SELECTEDVALUE(dim_date[Year], "All Years")
```

### 7.4 Verify a measure works

1. Click anywhere on a blank report canvas.
2. In the Fields pane, tick the checkbox next to `Total Revenue` (under whatever table you put it).
3. A card visual appears showing **$2,297,201** (or similar). 
4. That's your total revenue! Right-click it → **Delete** (we'll place proper visuals next).

> **Common beginner confusion:** if a measure name is used by ANOTHER measure (like `[Total Revenue]` inside `Revenue YoY Growth %`), that's intentional — measures can call other measures. Don't worry about it.

---

<a name="part-8"></a>
## PART 8 — BUILD PAGE 1: EXECUTIVE OVERVIEW

### 8.1 Rename the page

1. Look at the bottom of the screen — there's a tab labeled "Page 1".
2. Double-click it. Type **Executive Overview**. Press Enter.

### 8.2 Add a dark background

1. On the right side of the screen, click the **Format** icon (a paint-roller icon, at the top of the Visualizations pane).
2. Scroll down and find **Canvas background**.
3. Turn it **On**.
4. Click the color box and type **#1E293B** (a dark slate color), press Enter.
5. Set **Transparency** to 0.
6. While you're here, look for **Page size** → ensure **Width 16** and **Height 9** (16:9).

### 8.3 Add the 5 KPI cards (top-left area)

We'll build ONE card, then copy it 4 times.

1. In the **Visualizations** pane (right side, under Format), click the visual called **Card** (icon looks like a rectangle with a number, or use "Card (new)").
2. A blank card appears in the middle of the canvas. Drag it to the top-left corner.
3. In the **Fields** pane, drag `Total Revenue` (your measure) into the **Fields** box of the card (under Visualizations).
4. The card now shows **2.30M** (or $2.3M). 
5. **Copy it:** click the card, press **Ctrl+C**, then **Ctrl+V**. Drag the copy to the right of the first. Do this until you have 5 cards in a row.
6. Change each card's measure (click the card → in the Fields pane, drag the new measure into the Fields box, replacing the old):
   - Card 1: `Total Revenue`
   - Card 2: `Total Profit`
   - Card 3: `Total Orders`
   - Card 4: `Total Customers`
   - Card 5: `Profit Margin %`

### 8.4 Add slicers (filters for the user) — top-right

1. Click the **Slicer** visual in the Visualizations pane.
2. Drag it to the top-right.
3. In the Fields pane, drag `dim_date[Year]` into the slicer's **Field** box.
4. A list of years (2014, 2015, 2016, 2017) appears. Users can click these to filter everything.
5. Add a second slicer below it with `dim_products[Category]`.

### 8.5 Add the revenue & profit trend line chart (center)

1. Click the **Line chart** visual (a line going up).
2. Drag the chart to the center of the canvas (below the cards).
3. Set its fields:
   - **X-axis:** `dim_date[Date]` (or `dim_date[Year-Month]`)
   - **Y-axis:** drag BOTH `Total Revenue` AND `Total Profit`
4. You now see revenue and profit over time.

### 8.6 Add category donut (bottom-left)

1. Click the **Donut chart** visual (a circle with a hole).
2. Drag it to the bottom-left.
3. Set fields:
   - **Legend:** `dim_products[Category]`
   - **Values:** `Total Revenue`

### 8.7 Add sub-category bar chart (bottom-center)

1. Click the **Stacked column chart** or **Clustered column chart** visual.
2. Drag it to the bottom-center.
3. Set fields:
   - **X-axis:** `dim_products[Sub-Category]`
   - **Y-axis:** `Total Revenue`

### 8.8 Add the state map (bottom-right)

1. Click the **Filled map** visual (a map-shaped icon).
2. Drag it to the bottom-right.
3. Set fields:
   - **Location:** `dim_geography[State]`
   - **Color saturation:** `Total Revenue`
4. If the map shows blank/grey: it needs an internet connection for Bing maps. If it still fails, replace it with a **Bar chart** of Top 10 States (X-axis: `dim_geography[State]`, Y-axis: `Total Revenue`). That's totally fine.

### 8.9 Add a title text box

1. On the ribbon, go to **Insert** → **Text box**.
2. Type: **Superstore Sales Performance**.
3. Use the Format pane to make the text big (size 32), bold, and white.

### 8.10 Test Page 1

Click one of the years in the slicer → ALL charts update. Click a category in the donut → everything filters. Click the slicer's little eraser icon to clear.

---

<a name="part-9"></a>
## PART 9 — BUILD PAGE 2: PROFITABILITY DEEP-DIVE

This is the page that wins interviews. It shows your biggest insight: **discounts destroy profit.**

### 9.1 New page

1. Click the **+** sign next to the "Executive Overview" tab at the bottom to add a page.
2. Double-click the tab → rename to **Profitability**.
3. Repeat 8.2 to give it the same dark background.

### 9.2 KPI cards

1. Add 4 **Card** visuals (same method as 8.3) in a row across the top:
   - `Total Profit`
   - `Loss Orders`
   - `Loss Rate %`
   - `Potential Profit Recovery`

### 9.3 Discount band bar chart (the hero visual)

1. Click the **Clustered column chart** visual.
2. Set fields:
   - **X-axis:** `fact_orders[Discount Band]`
   - **Y-axis:** `Total Profit`
3. This is the money chart: the "No Discount" bar is tall and positive; the "30%+" bar is negative.
4. **Format it to show the story:**
   - Click the chart → **Format** (paint roller).
   - Find **Data colors** → turn **Color saturation** off, and add a conditional format:
     - Under "Data colors", set **Color saturation** from `Default color` to **Conditional formatting** (fx icon).
     - Format by: `Total Profit` → click the fx → Minimum = red, Maximum = green. Click OK.
   - Now profitable bands are green, losing bands are red. This looks incredible in interviews.

### 9.4 Combo chart: revenue by sub-category with margin line

1. Click the **Combo chart** visual (columns + line).
2. Set fields:
   - **Shared axis:** `dim_products[Sub-Category]`
   - **Column values:** `Total Revenue`
   - **Line values:** `Profit Margin %`
3. In Format, find **Y-axis** for the line and set **Show secondary** to On (there may be a toggle in the visual's formatting for the line series).

### 9.5 Top & bottom states bar chart

1. **Clustered bar chart** visual.
2. **Y-axis:** `dim_geography[State]`
3. **X-axis:** `Total Profit`
4. In the Visualizations pane's **Filters** section (bottom of the pane):
   - Drag `dim_geography[State]` into "Filters on this visual".
   - Filter type: **Top N**.
   - Show items: **Top 15** by `Total Profit`.
5. Apply the same conditional color formatting from 9.3 (red/green by value) so losing states are red.

### 9.6 Sub-category profit table

1. Click the **Table** visual.
2. Drag `dim_products[Sub-Category]` into Columns.
3. Drag `Total Revenue`, `Total Profit`, `Profit Margin %` into Columns too.
4. In **Format** → **Conditional formatting** → **Background color** on the `Total Profit` column → green/red by value.
5. This table is great for the interview: you can point at Tables & Bookcases losing money.

### 9.7 Insight callout (text box)

1. Insert → Text box.
2. Paste: **"Discounts >20% destroy margin — full-price orders run at 34% margin vs -8% for discounted orders. Estimated recoverable profit: $138K."**
3. Make it bold, white text.

### 9.8 Add a discount slicer (top-right)

1. Add a **Slicer** visual.
2. Field: `fact_orders[Discount]`.
3. In the Format pane, change slicer **Style** to **Range** (a slider). Users can now drag a slider to see profit at any discount level — a very interactive "aha" demo.

---

<a name="part-10"></a>
## PART 10 — BUILD PAGE 3: CUSTOMER SEGMENTATION (RFM)

RFM = Recency, Frequency, Monetary. It's the industry-standard way to value customers. The scores are already computed in `customer_rfm_analysis.csv`.

### 10.1 New page

1. **+** sign → rename tab to **Customers**.

### 10.2 KPI cards

Add 4 cards across the top:
- `Total Customers`
- `Avg Customer LTV`
- `Repeat Purchase Rate %`
- `Champions Count`

### 10.3 Treemap of segments (center-left)

1. **Treemap** visual (a box of nested rectangles).
2. **Group:** `customer_rfm_analysis[Customer Segment]`
3. **Values:** `Customers in Segment`
4. This shows which segments have the most customers (bigger rectangle = more customers).

### 10.4 Scatter chart: Frequency vs Monetary (center-right)

1. **Scatter chart** visual (bubble chart).
2. Fields:
   - **Values:** `customer_rfm_analysis[Customer ID]`
   - **X-axis:** `customer_rfm_analysis[Frequency]`
   - **Y-axis:** `customer_rfm_analysis[Monetary]`
   - **Color saturation:** `customer_rfm_analysis[Customer Segment]`
3. This shows clusters of Champions (top-right = buy often, spend a lot) vs At Risk (bottom-right).
4. Add a **Legend** by putting `Customer Segment` in the Legend field for a cleaner look.

### 10.5 Avg LTV by segment (bottom-left)

1. **Bar chart.**
2. **Y-axis:** `customer_rfm_analysis[Customer Segment]`
3. **X-axis:** `Avg Customer LTV`

### 10.6 Matrix: segment × year (bottom-right)

1. **Matrix** visual (a pivot table).
2. **Rows:** `customer_rfm_analysis[Customer Segment]`
3. **Columns:** `dim_date[Year]` — wait, this table isn't linked to dim_date.

   **Fix:** link `customer_rfm_analysis[Customer ID]` to `fact_orders[Customer ID]`? That would double-count. Instead, simplest approach: use `customer_rfm_analysis[First_Order]`? Too complex.
   
   **Easy alternative:** put **Rows:** `customer_rfm_analysis[Customer Segment]` and **Values:** `Segment Revenue`. That alone is a strong matrix. (Skip the Year column — you already show year trends on Page 1.)

### 10.7 Segment slicer (top-right)

1. **Slicer** visual → Field: `customer_rfm_analysis[Customer Segment]` → set Style to **Tile** (pretty colored tiles).

### 10.8 Insight text box

Paste: **"124 Champions generate ~$5.2K average revenue each. 261 customers are At Risk or Lost — a ~$600K retention opportunity. Win-back campaigns for At Risk; loyalty program for Potential Loyalists."**

---

<a name="part-11"></a>
## PART 11 — BUILD PAGE 4: OPERATIONS & SHIPPING

### 11.1 New page → rename to **Operations**.

### 11.2 KPI cards

- `Avg Shipping Days`
- `Total Orders`
- `Late Order Rate %`

### 11.3 Orders by ship mode (center-left)

1. **Bar chart.**
2. **Y-axis:** `fact_orders[Ship Mode]`
3. **X-axis:** `Total Orders`

### 11.4 Avg shipping days by ship mode (center-right)

1. **Bar chart.**
2. **Y-axis:** `fact_orders[Ship Mode]`
3. **X-axis:** `Avg Shipping Days`

### 11.5 Revenue by day of week (right)

1. **Column chart.**
2. **X-axis:** `fact_orders[Order Day of Week]`
3. **Y-axis:** `Total Revenue`
4. Sort problem: Power BI sorts alphabetically. To sort Mon→Sun:
   - In the **Data** view, select `fact_orders`.
   - Click **New column**, paste:
     ```
     Day Sort = SWITCH(fact_orders[Order Day of Week],
         "Monday", 1, "Tuesday", 2, "Wednesday", 3, "Thursday", 4,
         "Friday", 5, "Saturday", 6, "Sunday", 7)
     ```
   - Back on the chart, select the X-axis → choose `Order Day of Week`, then go to the **Column tools** ribbon → **Sort by column** → `Day Sort`.

### 11.6 Revenue trend with moving average (bottom)

1. **Line chart.**
2. **X-axis:** `dim_date[Date]` → use the hierarchy drill-down (Year → Quarter → Month).
3. **Y-axis:** `Total Revenue`.
4. In the Analytics pane (little magnifying-glass icon at top of Visualizations):
   - Click **+** next to **Average line** → add it. Choose the Y-axis measure `Total Revenue`.
   - (Optionally add a **Forecast** of 3 periods to show you know forecasting.)

### 11.7 Revenue by region × quarter (bottom-right)

1. **Stacked column chart.**
2. **X-axis:** `fact_orders[Year-Quarter]`
3. **Legend:** `dim_geography[Region]`
4. **Y-axis:** `Total Revenue`

---

<a name="part-12"></a>
## PART 12 — ADD NAVIGATION BUTTONS & BOOKMARKS (WOW FACTOR)

This makes your dashboard feel like a real product.

### 12.1 Create bookmarks for each page

1. On the ribbon, go to the **View** tab → tick **Bookmarks pane** (a panel opens on the right).
2. Click **Add** — it saves the current view as a bookmark. Rename it (double-click) to **Overview**.
3. Switch to Page 2 (Profitability) by clicking its tab. Click **Add** again → rename **Profitability**.
4. Repeat for **Customers** and **Operations**.

### 12.2 Add navigation buttons to every page

1. Go to **Insert** → **Buttons** → **Chevron** (or "Blank"). 
2. With the button selected, on the right click the **Format** pane.
3. Find **Button text** → set **On** → type **Overview**.
4. Find **Action** → set **On**:
   - **Type:** Bookmark
   - **Bookmark:** Overview
5. Repeat, adding buttons for **Profitability**, **Customers**, **Operations** — each with its own Action → Bookmark.
6. Copy (Ctrl+C / Ctrl+V) this set of buttons to every page so users can navigate from anywhere.

### 12.3 Test it

Click the buttons while holding... no, just click them normally. The dashboard should jump between pages.

---

<a name="part-13"></a>
## PART 13 — SAVE, PUBLISH & SHARE

### 13.1 Save

1. Click **File** → **Save As**.
2. Go to `C:\Users\ASUS\OneDrive\Desktop\Data Analyst\powerbi\`.
3. Name it: **E-Commerce_Analytics_Dashboard.pbix**.
4. Click **Save**.

### 13.2 Publish to Power BI Service (free)

> **IMPORTANT — sign-in is ONLY needed for this publishing step.**
> Everything you built (Pages 1–4, measures, buttons) works 100% offline. If the sign-in window pops up and asks for a **school or organization email**, do this:
> - Click the **X** (close) or **Not now / Skip**. Power BI Desktop keeps working normally.
> - Build and save your dashboard first. Deal with publishing AFTER the dashboard is finished.

**Step 1 — Create your free Power BI account in a browser (personal email works):**

1. Open your web browser and go to: `https://app.powerbi.com`
2. Click **Start free** (or **Try free**).
3. On the sign-in page, enter your **personal email** (Gmail, Yahoo, Outlook, Hotmail — any works). If it says "We couldn't find an account", click **Create one!** and follow the prompts.
4. You'll be asked to fill a short form (name, country, company = type anything like "Self" / "Student") and accept the terms.
5. Wait a moment — you now have a **free Power BI account** linked to your personal email.

**Step 2 — Sign in to Power BI Desktop with that email:**

1. Go back to Power BI Desktop.
2. Click the **Sign in** link (top-right corner of the window).
3. In the login box, type the **same personal email** you used in Step 1.
4. If the login page only shows a "Work or school account" box:
   - Look for the link **"Personal account"** or **"Use another account"** and click it.
   - OR click **Sign in options** → choose **Microsoft account**.
   - OR if it still refuses, close it, reopen `https://app.powerbi.com`, make sure you're signed in there (top-right shows your email), then click **Sign in** in Desktop again.

**Step 3 — Publish:**

1. With sign-in working, click **Home** → **Publish** (top-right of the ribbon).
2. Choose a workspace — the default is **My workspace** → click **Select**.
3. Wait for the upload. When it finishes, click **Open 'E-Commerce_Analytics_Dashboard.pbix' in Power BI**.
4. Your dashboard is now online and gets a shareable link.

> **If you truly cannot get an account, you still have options:**
> - Power BI Desktop's **File → Export → Export to PDF** works WITHOUT any sign-in. Export your 4 pages as a PDF and attach it to job applications.
> - Export charts as images (click a visual → right-click → Export data or copy image) for your resume.
> - Publishing is a "nice to have" — a polished local `.pbix` file you can demo live on a screen is already interview-ready.

### 13.3 Share with recruiters

1. In the Power BI Service (browser), open your report.
2. Use **File → Embed report → Website or portal** → copy the **embed link**.
3. Put this link in your resume/GitHub README — recruiters can click and interact with your live dashboard.

### 13.4 Export pages as PDF (for resumes/appendix)

1. In Power BI Service, click **File → Export → Export to PDF** (or in Desktop, **File → Export → Export to PDF**).
2. Attach the PDF to job applications.

---

<a name="part-14"></a>
## PART 14 — TROUBLESHOOTING COMMON ERRORS

| Symptom | Cause | Fix |
|---------|-------|-----|
| A measure shows `(Blank)` | No data matches the current filter, or a column name typo | Check spelling of table/column names in the formula; clear slicers |
| Measure returns an error | Missing relationship, or column referenced from a table not linked to the visual's table | Go to Model view, verify relationships from Part 4 |
| Columns named `Column1`, `Column2`... | First row wasn't used as headers on import | Part 3.4: Power Query → **Use First Row as Headers**, then delete the leftover text row |
| `Column 'Product ID' ... contains a duplicate value` when creating a relationship | A dimension table has duplicate keys (same ID with slightly different names in the raw data) | Re-run `python scripts/01_data_cleaning.py` (dedupes by ID), then in Power BI click **Home → Refresh** to reload the fixed files |
| `A single value for column 'Discount' ... cannot be determined` | You created a formula with **New measure** instead of **New column** (row-by-row formulas need a column) | Part 6.2 Step A: delete the wrong item, then Step B: recreate it via **Data view → Table tools → New column** |
| `The syntax for 'Total' is incorrect` (or any syntax error when adding measures) | You pasted MULTIPLE measures into the formula bar at once — it accepts only ONE formula per measure | Press **Esc** to cancel, delete any broken measure, then paste **one measure at a time** (Part 7.3) |
| Dates show as text / "ABC" | Imported as text | Part 3: change type to Date in Power Query |
| Map is empty | No internet / Bing blocked | Replace with a bar chart of top states |
| Line chart shows nothing | X-axis is a date but no data | Use `dim_date[Date]` (marked date table) not the fact table dates |
| "Cannot find column" error in DAX | Wrong table/column name | Column names with spaces go in brackets: `fact_orders[Order Date]`, `fact_orders[Profit Margin (%)]` |
| Numbers look like 2.3M instead of $2,297,201 | Display format | Click visual → Format → **Field formatting** → select the measure → set **Thousands separator** and **2 decimal places** |
| Profit Margin % shows 0.12 instead of 12% | Format not applied | Format → Field formatting → Percent → 1 decimal |
| A slicer doesn't filter a chart | No relationship between the slicer's table and the chart's table | Model view → check relationships |
| Slow loading | Too many visuals | Turn off auto date/time (File → Options → Data Load → deselect "Auto date/time") and rebuild model |
| "Can't sign in — it asks for a school or organization email" | Sign-in is only needed for publishing; personal accounts work if you sign up via the web first | Part 13.2: skip sign-in while building; create a free account at `https://app.powerbi.com` with your personal email, then sign in with the same email |

---

<a name="part-15"></a>
## PART 15 — GLOSSARY OF POWER BI WORDS

- **Visual** — a chart, card, table, or map. Anything you drag onto the canvas.
- **Canvas** — the blank page you draw your dashboard on.
- **Fields pane** — the right panel listing all your tables and columns.
- **Visualizations pane** — the right panel with chart icons.
- **Format pane** — the paint-roller icon; where you style colors, fonts, titles.
- **Slicer** — a dropdown/slider users click to filter the whole page.
- **Measure** — a DAX formula that computes a number depending on filters.
- **Calculated column** — a formula that adds a column to a table (per row).
- **DAX** — the formula language of Power BI (like Excel formulas but for whole tables).
- **Star schema** — one fact table connected to dimension tables.
- **Relationship** — the link between two tables via a common column.
- **Cross filter direction** — whether filters flow both ways between tables (keep it "Single").
- **Power Query** — the built-in data-cleaning tool (Transform Data).
- **Publish** — uploading your desktop file to the cloud Power BI Service.
- **Bookmark** — a saved snapshot of a page; used with buttons for navigation.

---

## FINAL CHECKLIST — before you show this to anyone

- [ ] All 4 pages exist: Executive Overview, Profitability, Customers, Operations
- [ ] Page 1 has 5 KPI cards + line chart + donut + category bar + map
- [ ] Page 2 has the **discount band chart** with red/green conditional colors
- [ ] Page 3 has the RFM treemap + scatter + matrix
- [ ] Page 4 has shipping charts + day-of-week sorted correctly
- [ ] Every page has navigation buttons (Overview / Profitability / Customers / Operations)
- [ ] Every currency shows thousands separators and 2 decimals
- [ ] Profit Margin % shows as a percent
- [ ] Negative values are red
- [ ] Slicers work and clear correctly
- [ ] Saved as `E-Commerce_Analytics_Dashboard.pbix` in the `powerbi/` folder
- [ ] Published to Power BI Service and you have a share link
- [ ] You can explain the discount insight out loud in 30 seconds

## What to say in the interview

> "My biggest insight was that discounts above 20% turn profitable orders into losses. Orders without discounts run a 34% margin, but discounted orders average -8%. I built a Power BI page that visualizes this by discount band, quantified the recoverable profit at about $138K, and recommended capping discounts at 20%."

If you can say that sentence naturally, the interview is basically won. Good luck!
