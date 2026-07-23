"""
Sprint Burndown Chart Generator
Generates a professional burn chart visualization for the Cyber Complaint and Case Management System
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
from datetime import datetime, timedelta

def generate_burndown_chart(output_file='burndown_chart.png'):
    """
    Generate a project burndown chart spanning full timeline from Jan 1 - Apr 20, 2026
    """
    
    # Project timeline: Jan 1 - Apr 20, 2026 (110 days total)
    # Using weekly data points for clarity
    days = np.arange(0, 16)  # 16 weeks (0-15 weeks)
    
    # Ideal burndown: linear decreasing
    total_story_points = 235  # Total estimated work
    ideal_points = [total_story_points - (total_story_points / 15 * week) for week in days]
    
    # Actual burndown: ahead of schedule
    actual_points = [235, 215, 195, 170, 145, 125, 105, 85, 70, 55, 40, 25, 15, 8, 2, 0]
    
    # Week labels (every week starting Jan 1)
    week_labels = ['Wk1(Jan1-5)', 'Wk2(Jan6-12)', 'Wk3(Jan13-19)', 'Wk4(Jan20-26)', 
                   'Wk5(Jan27-Feb2)', 'Wk6(Feb3-9)', 'Wk7(Feb10-16)', 'Wk8(Feb17-23)',
                   'Wk9(Feb24-Mar2)', 'Wk10(Mar3-9)', 'Wk11(Mar10-16)', 'Wk12(Mar17-23)',
                   'Wk13(Mar24-30)', 'Wk14(Mar31-Apr6)', 'Wk15(Apr7-13)', 'Wk16(Apr14-20)']
    
    # Create figure and axis with larger size
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Plot lines
    ax.plot(days, ideal_points, 'o-', label='Ideal Dev', color='#FFB84D', linewidth=2.5, markersize=6, alpha=0.8)
    ax.plot(days, actual_points, 'o-', label='Actual Dev', color='#4472C4', linewidth=2.5, markersize=6)
    
    # Fill area between curves
    ax.fill_between(days, ideal_points, actual_points, alpha=0.1, color='#4472C4')
    
    # Grid
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)
    
    # Labels and title
    ax.set_xlabel('Project Timeline (Weekly)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Story Points Remaining', fontsize=12, fontweight='bold')
    ax.set_title('Project Burndown Chart - Jan 1 to Apr 20, 2026', fontsize=16, fontweight='bold', pad=20)
    
    # X-axis - Show every other week
    x_ticks = np.arange(0, 16, 2)
    x_labels = [week_labels[i] for i in x_ticks]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, fontsize=9)
    
    # Y-axis
    ax.set_ylim(0, 250)
    ax.set_xlim(-0.5, 15.5)
    ax.set_yticks(np.arange(0, 250, 25))
    ax.tick_params(labelsize=9)
    
    # Legend for lines
    ax.legend(loc='upper right', fontsize=10, framealpha=0.95, edgecolor='black')
    
    # Add phase descriptions on the right side
    phases = [
        {
            'title': 'PHASE 1: JAN 01-15',
            'description': 'Planning &\nRequirements\n(Weeks 1-3)',
            'y_pos': 0.88
        },
        {
            'title': 'PHASE 2: JAN 16-FEB 14',
            'description': 'Design &\nArchitecture\n(Weeks 4-7)',
            'y_pos': 0.72
        },
        {
            'title': 'PHASE 3: FEB 15-APR 08',
            'description': 'Development\nUser, Complaint,\nCase Mgmt\n(Weeks 8-13)',
            'y_pos': 0.48
        },
        {
            'title': 'PHASE 4: APR 09-14',
            'description': 'Testing\nUnit, Integration\nSecurity\n(Weeks 14-15)',
            'y_pos': 0.25
        },
        {
            'title': 'PHASE 5: APR 15-20',
            'description': 'Deployment &\nGo-Live\n✓ DELIVERED\n(Week 16)',
            'y_pos': 0.08
        }
    ]
    
    # Add colored boxes with descriptions
    colors = ['#E7E6E6', '#F2DCCE', '#F4CCCC', '#D5D8F3', '#E2EFDA']
    
    for i, phase in enumerate(phases):
        # Add circular number indicator
        circle = plt.Circle((1.09, phase['y_pos']), 0.025, 
                           color=colors[i], ec='#A4A4A4', linewidth=1.5,
                           transform=fig.transFigure, zorder=10)
        fig.patches.append(circle)
        
        # Add number text
        fig.text(1.092, phase['y_pos'], str(i+1), 
                fontsize=9, fontweight='bold', ha='center', va='center',
                transform=fig.transFigure, zorder=11, color='#404040')
        
        # Add phase title (bold date range)
        fig.text(1.13, phase['y_pos'] + 0.015, phase['title'], 
                fontsize=10, fontweight='bold', va='center',
                transform=fig.transFigure, color='#404040')
        
        # Add description
        fig.text(1.13, phase['y_pos'] - 0.025, phase['description'], 
                fontsize=8.5, va='top', style='normal',
                transform=fig.transFigure, color='#595959',
                wrap=True, multialignment='left')
    
    # Add legend box title
    fig.text(1.09, 0.98, 'PROJECT PHASES (5)', 
            fontsize=10, fontweight='bold', va='top',
            transform=fig.transFigure, color='#404040')
    
    # Adjust layout to prevent text cutoff
    plt.subplots_adjust(right=0.72, left=0.08, top=0.93, bottom=0.1)
    
    # Save the figure
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"✓ Burn chart generated successfully: {output_file}")
    
    # Also display the chart
    plt.show()
    
    return output_file


if __name__ == '__main__':
    generate_burndown_chart('burndown_chart.png')
