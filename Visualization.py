import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Create a DataFrame for better data handling and seaborn integration
data = pd.DataFrame({
    'fiscal_years': ['FY21/22', 'FY22/23', 'FY23/24'],
    'revenue': [18.3, 22.8, 29.0],  # in billion £
    'net_profit': [-0.4, -0.1, 2.2],  # in billion £, profit before tax & exceptional items
    'free_cash_flow': [-1.1, 0.5, 2.3],  # in billion £
    'net_debt': [3.2, 3.0, 0.7],  # in billion £
    'unit_sales': [376381, 354662, 431733]  # number of units
})

# Set the seaborn theme for all plots
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 12})

# Custom color palette
palette = sns.color_palette("viridis", 5)

# Chart 1: Revenue Trend with enhanced styling
plt.figure(figsize=(10, 6))
ax = sns.lineplot(x='fiscal_years', y='revenue', data=data, marker='o', markersize=10, 
                 color=palette[0], linewidth=3)
                 
# Add value annotations
for i, val in enumerate(data['revenue']):
    ax.text(i, val + 0.3, f'£{val}B', ha='center', fontweight='bold')

plt.title('Revenue Growth Trend', fontsize=16, fontweight='bold')
plt.xlabel('Fiscal Year', fontsize=14)
plt.ylabel('Revenue (Billion £)', fontsize=14)
sns.despine(left=True, bottom=True)
plt.tight_layout()
plt.savefig("enhanced_revenue_trend.png", dpi=300)
plt.show()

# Chart 2: Net Profit Trend with enhanced styling
plt.figure(figsize=(10, 6))
bars = sns.barplot(x='fiscal_years', y='net_profit', data=data, 
                  palette=['#FF5252' if x < 0 else '#4CAF50' for x in data['net_profit']])

# Add value annotations
for i, bar in enumerate(bars.patches):
    value = data['net_profit'].iloc[i]
    text_color = 'white' if value < 0 else 'black'
    height = bar.get_height()
    if height < 0:
        y_pos = height - 0.2
    else:
        y_pos = height + 0.1
    bars.text(bar.get_x() + bar.get_width()/2., y_pos, 
             f'£{value}B', ha='center', va='bottom', fontweight='bold', color=text_color)

plt.title('Net Profit Before Tax & Exceptions', fontsize=16, fontweight='bold')
plt.xlabel('Fiscal Year', fontsize=14)
plt.ylabel('Net Profit (Billion £)', fontsize=14)
plt.axhline(0, color='black', linewidth=1.5, alpha=0.7)
sns.despine(left=True, bottom=True)
plt.tight_layout()
plt.savefig("enhanced_net_profit_trend.png", dpi=300)
plt.show()

# Chart 3: Free Cash Flow with enhanced styling
plt.figure(figsize=(10, 6))
ax = sns.lineplot(x='fiscal_years', y='free_cash_flow', data=data, marker='s', markersize=10, 
                 color=palette[2], linewidth=3)

# Fill the area under the curve with gradient
ax.fill_between(range(len(data)), data['free_cash_flow'], alpha=0.3, color=palette[2])

# Add value annotations
for i, val in enumerate(data['free_cash_flow']):
    y_offset = 0.15 if val < 0 else 0.15
    text_color = 'red' if val < 0 else 'green'
    ax.text(i, val + y_offset, f'£{val}B', ha='center', fontweight='bold', color=text_color)
    
plt.title('Free Cash Flow Progression', fontsize=16, fontweight='bold')
plt.xlabel('Fiscal Year', fontsize=14)
plt.ylabel('Free Cash Flow (Billion £)', fontsize=14)
plt.axhline(0, color='black', linewidth=1.5, alpha=0.7)
sns.despine(left=True, bottom=True)
plt.tight_layout()
plt.savefig("enhanced_free_cash_flow.png", dpi=300)
plt.show()

# Chart 4: Net Debt with enhanced styling
plt.figure(figsize=(10, 6))
ax = sns.lineplot(x='fiscal_years', y='net_debt', data=data, marker='^', markersize=10, 
                 color=palette[3], linewidth=3)

# Add value annotations with downward trend highlighting
for i, val in enumerate(data['net_debt']):
    ax.text(i, val + 0.15, f'£{val}B', ha='center', fontweight='bold')
    
# Show the decrease with arrows
for i in range(len(data) - 1):
    if data['net_debt'].iloc[i+1] < data['net_debt'].iloc[i]:
        plt.annotate('', 
                    xy=(i+1, data['net_debt'].iloc[i+1]), 
                    xytext=(i, data['net_debt'].iloc[i]),
                    arrowprops=dict(arrowstyle='->', color='green', lw=2, alpha=0.5))

plt.title('Net Debt Reduction', fontsize=16, fontweight='bold')
plt.xlabel('Fiscal Year', fontsize=14)
plt.ylabel('Net Debt (Billion £)', fontsize=14)
sns.despine(left=True, bottom=True)
plt.tight_layout()
plt.savefig("enhanced_net_debt_trend.png", dpi=300)
plt.show()

# Chart 5: Unit Sales with enhanced styling
plt.figure(figsize=(10, 6))
ax = sns.lineplot(x='fiscal_years', y='unit_sales', data=data, marker='o', markersize=10, 
                 color=palette[4], linewidth=3)

# Add value annotations with formatted numbers
for i, val in enumerate(data['unit_sales']):
    ax.text(i, val + 10000, f'{val:,}', ha='center', fontweight='bold')

plt.title('Vehicle Unit Sales Performance', fontsize=16, fontweight='bold')
plt.xlabel('Fiscal Year', fontsize=14)
plt.ylabel('Units Sold', fontsize=14)
sns.despine(left=True, bottom=True)
plt.tight_layout()
plt.savefig("enhanced_unit_sales_trend.png", dpi=300)
plt.show()

# Bonus: Combined Dashboard-style visualization
plt.figure(figsize=(15, 12))

# Create a 3x2 grid for subplots
grid = plt.GridSpec(3, 2, hspace=0.4, wspace=0.3)

# Revenue trend - Top left
ax1 = plt.subplot(grid[0, 0])
sns.lineplot(x='fiscal_years', y='revenue', data=data, marker='o', ax=ax1, 
            color=palette[0], linewidth=3, markersize=8)
for i, val in enumerate(data['revenue']):
    ax1.text(i, val + 0.3, f'£{val}B', ha='center', fontsize=10, fontweight='bold')
ax1.set_title('Revenue (Billion £)', fontweight='bold')
sns.despine(ax=ax1, left=True, bottom=True)

# Net profit - Top right
ax2 = plt.subplot(grid[0, 1])
bars = sns.barplot(x='fiscal_years', y='net_profit', data=data, ax=ax2,
                  palette=['#FF5252' if x < 0 else '#4CAF50' for x in data['net_profit']])
for i, bar in enumerate(bars.patches):
    value = data['net_profit'].iloc[i]
    text_color = 'white' if value < 0 else 'black'
    height = bar.get_height()
    if height < 0:
        y_pos = height - 0.15
    else:
        y_pos = height + 0.1
    ax2.text(bar.get_x() + bar.get_width()/2., y_pos, 
            f'£{value}B', ha='center', fontsize=10, fontweight='bold', color=text_color)
ax2.set_title('Net Profit (Billion £)', fontweight='bold')
ax2.axhline(0, color='black', linewidth=1.5, alpha=0.7)
sns.despine(ax=ax2, left=True, bottom=True)

# Free Cash Flow - Middle left
ax3 = plt.subplot(grid[1, 0])
sns.lineplot(x='fiscal_years', y='free_cash_flow', data=data, marker='s', ax=ax3,
            color=palette[2], linewidth=3, markersize=8)
ax3.fill_between(range(len(data)), data['free_cash_flow'], alpha=0.3, color=palette[2])
for i, val in enumerate(data['free_cash_flow']):
    y_offset = 0.15 if val < 0 else 0.15
    text_color = 'red' if val < 0 else 'green'
    ax3.text(i, val + y_offset, f'£{val}B', ha='center', fontsize=10, fontweight='bold', color=text_color)
ax3.set_title('Free Cash Flow (Billion £)', fontweight='bold')
ax3.axhline(0, color='black', linewidth=1.5, alpha=0.7)
sns.despine(ax=ax3, left=True, bottom=True)

# Net Debt - Middle right
ax4 = plt.subplot(grid[1, 1])
sns.lineplot(x='fiscal_years', y='net_debt', data=data, marker='^', ax=ax4,
            color=palette[3], linewidth=3, markersize=8)
for i, val in enumerate(data['net_debt']):
    ax4.text(i, val + 0.15, f'£{val}B', ha='center', fontsize=10, fontweight='bold')
ax4.set_title('Net Debt (Billion £)', fontweight='bold')
sns.despine(ax=ax4, left=True, bottom=True)

# Unit Sales - Bottom span
ax5 = plt.subplot(grid[2, :])
sns.lineplot(x='fiscal_years', y='unit_sales', data=data, marker='o', ax=ax5,
            color=palette[4], linewidth=3, markersize=8)
for i, val in enumerate(data['unit_sales']):
    ax5.text(i, val + 10000, f'{val:,}', ha='center', fontsize=10, fontweight='bold')
ax5.set_title('Unit Sales', fontweight='bold')
sns.despine(ax=ax5, left=True, bottom=True)

plt.suptitle('Financial Performance Dashboard FY21/22 - FY23/24', fontsize=20, fontweight='bold', y=0.98)
plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.savefig("financial_dashboard.png", dpi=300)
plt.show()