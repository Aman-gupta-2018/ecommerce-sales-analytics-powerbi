"""
Generate Star Schema Diagram PNG for README
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Background
fig.patch.set_facecolor('#0F172A')
ax.set_facecolor('#0F172A')

def draw_box(ax, x, y, w, h, title, cols, is_fact=False):
    bg_color = '#1E293B' if not is_fact else '#1E1B4B'
    header_color = '#3B82F6' if not is_fact else '#6366F1'
    border_color = '#60A5FA' if not is_fact else '#818CF8'
    
    # Outer box
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5", 
                                  ec=border_color, fc=bg_color, lw=2)
    ax.add_patch(rect)
    
    # Title box
    t_rect = patches.Rectangle((x, y + h - 8), w, 8, fc=header_color, ec='none')
    ax.add_patch(t_rect)
    ax.text(x + w/2, y + h - 4, title, color='white', weight='bold', 
            fontsize=11, ha='center', va='center')
    
    # Columns
    for i, col in enumerate(cols):
        ax.text(x + 3, y + h - 14 - (i * 6), col, color='#E2E8F0', 
                fontsize=8, va='center')

# Fact Table in Center
draw_box(ax, 38, 30, 24, 40, "fact_orders (Fact)", [
    "Row ID (PK)",
    "Order ID",
    "Order Date (FK)",
    "Customer ID (FK)",
    "Product ID (FK)",
    "Geo ID (FK)",
    "Sales",
    "Profit",
    "Discount",
    "Quantity"
], is_fact=True)

# Dimension Tables around
draw_box(ax, 5, 60, 22, 30, "dim_customers", [
    "Customer ID (PK)",
    "Customer Name",
    "Segment"
])

draw_box(ax, 73, 60, 22, 30, "dim_products", [
    "Product ID (PK)",
    "Product Name",
    "Category",
    "Sub-Category"
])

draw_box(ax, 5, 10, 22, 30, "dim_geography", [
    "Geo ID (PK)",
    "City",
    "State",
    "Region",
    "Postal Code"
])

draw_box(ax, 73, 10, 22, 30, "dim_date", [
    "Date (PK)",
    "Year",
    "Quarter",
    "Month",
    "Month Name"
])

# Draw Relationship Lines
def draw_line(x1, y1, x2, y2, label="1 : N"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color='#94A3B8', lw=1.5))

draw_line(27, 75, 38, 55) # customer -> fact
draw_line(73, 75, 62, 55) # product -> fact
draw_line(27, 25, 38, 40) # geo -> fact
draw_line(73, 25, 62, 40) # date -> fact

plt.title("Star Schema Data Model (1:N Relationships)", color='white', 
          fontsize=14, weight='bold', pad=20)

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                        "outputs", "charts", "star_schema_model.png")
plt.savefig(out_path, dpi=200, bbox_inches='tight')
plt.close()
print(f"Star schema diagram saved to {out_path}")
