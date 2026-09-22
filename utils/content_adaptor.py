import re
import base64
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from textstat import flesch_reading_ease

class ContentAdaptor:
    def __init__(self):
        # Define adaptation rules after all methods are defined
        self.adaptation_rules = {}
        self._setup_adaptation_rules()
        
        # Visual content database
        self.visual_templates = {
            "mathematics": self.create_math_visuals,
            "science": self.create_science_visuals,
            "language": self.create_language_visuals,
            "history": self.create_history_visuals
        }
    
    def _setup_adaptation_rules(self):
        """Setup adaptation rules after all methods are defined"""
        self.adaptation_rules = {
            "ADHD": self.adapt_for_adhd,
            "Dyslexia": self.adapt_for_dyslexia,
            "Autism Spectrum": self.adapt_for_autism,
            "General": self.adapt_general
        }
    
    def adapt_content(self, content, profile, font_size=16):
        """Adapt content based on learning profile"""
        if profile in self.adaptation_rules:
            content = self.adaptation_rules[profile](content)
        
        # Apply font size and basic formatting
        content = self.apply_basic_formatting(content, font_size)
        return content
    
    def adapt_for_adhd(self, content):
        """Adapt content for ADHD learners"""
        # Break into smaller chunks
        paragraphs = content.split('\n\n')
        adapted_paragraphs = []
        
        for paragraph in paragraphs:
            if len(paragraph) > 100:
                # Split long paragraphs
                sentences = re.split(r'[.!?]+', paragraph)
                chunks = self.chunk_sentences(sentences, 2)
                adapted_paragraphs.extend(['. '.join(chunk) + '.' for chunk in chunks])
            else:
                adapted_paragraphs.append(paragraph)
        
        # Add visual markers and highlights
        adapted_content = "\n\n".join(adapted_paragraphs)
        adapted_content = self.add_highlights(adapted_content)
        adapted_content = self.add_visual_breaks(adapted_content)
        
        return adapted_content
    
    def adapt_for_dyslexia(self, content):
        """Adapt content for dyslexic learners"""
        # Simplify language
        content = self.simplify_language(content)
        
        # Add dyslexia-friendly formatting
        content = self.add_dyslexia_formatting(content)
        
        return content
    
    def adapt_for_autism(self, content):
        """Adapt content for autistic learners"""
        # Make language more literal and clear
        content = self.remove_idioms(content)
        content = self.add_explicit_instructions(content)
        content = self.add_visual_structure(content)
        
        return content
    
    def adapt_general(self, content):
        """General adaptation - minimal changes"""
        return content
    
    def chunk_sentences(self, sentences, chunk_size):
        """Group sentences into chunks"""
        return [sentences[i:i + chunk_size] for i in range(0, len(sentences), chunk_size)]
    
    def add_highlights(self, content):
        """Add highlighting for key concepts"""
        # Simple keyword highlighting - in real app, use NLP
        keywords = ["important", "key", "remember", "note", "example", "definition"]
        for keyword in keywords:
            content = re.sub(
                f'\\b{keyword}\\b', 
                f'**{keyword}**', 
                content, 
                flags=re.IGNORECASE
            )
        return content
    
    def add_visual_breaks(self, content):
        """Add visual breaks and markers"""
        lines = content.split('\n')
        adapted_lines = []
        
        for i, line in enumerate(lines):
            if line.strip() and not line.startswith('#') and len(line) > 20:
                adapted_lines.append(f"▸ {line}")
            else:
                adapted_lines.append(line)
            
            # Add occasional breaks
            if i % 3 == 0 and i > 0:
                adapted_lines.append("---")
        
        return '\n'.join(adapted_lines)
    
    def simplify_language(self, content):
        """Simplify complex language"""
        # Basic simplification rules
        replacements = {
            r'\butilize\b': 'use',
            r'\bapproximately\b': 'about',
            r'\bdemonstrate\b': 'show',
            r'\bfacilitate\b': 'help',
            r'\bapproximately\b': 'about',
            r'\brequire\b': 'need',
            r'\bassistance\b': 'help',
            r'\bterminate\b': 'end'
        }
        
        for pattern, replacement in replacements.items():
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        return content
    
    def add_dyslexia_formatting(self, content):
        """Add dyslexia-friendly formatting"""
        # Use shorter lines and clear spacing
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            if len(line) > 80:
                # Break long lines
                words = line.split()
                current_line = []
                current_length = 0
                
                for word in words:
                    if current_length + len(word) + 1 > 80:
                        formatted_lines.append(' '.join(current_line))
                        current_line = [word]
                        current_length = len(word)
                    else:
                        current_line.append(word)
                        current_length += len(word) + 1
                
                if current_line:
                    formatted_lines.append(' '.join(current_line))
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def remove_idioms(self, content):
        """Remove or explain idioms"""
        idioms = {
            "piece of cake": "very easy",
            "break a leg": "good luck",
            "hit the books": "study hard",
            "costs an arm and a leg": "very expensive",
            "bite the bullet": "face something difficult"
        }
        
        for idiom, meaning in idioms.items():
            content = content.replace(idiom, meaning)
        
        return content
    
    def add_explicit_instructions(self, content):
        """Make instructions more explicit"""
        instruction_patterns = [
            (r'([^.!?]*\bdo this\b[^.!?]*[.!?])', r'**Step:** \1'),
            (r'([^.!?]*\bfollow these steps\b[^.!?]*[.!?])', r'**Instructions:** \1'),
            (r'([^.!?]*\byou should\b[^.!?]*[.!?])', r'**Action:** \1')
        ]
        
        for pattern, replacement in instruction_patterns:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        return content
    
    def add_visual_structure(self, content):
        """Add clear visual structure"""
        # Ensure consistent heading hierarchy
        lines = content.split('\n')
        structured_lines = []
        
        for line in lines:
            if line.strip().startswith('##'):
                structured_lines.append(f"### {line.replace('##', '').strip()}")
            elif line.strip().startswith('#'):
                structured_lines.append(f"## {line.replace('#', '').strip()}")
            else:
                structured_lines.append(line)
        
        return '\n'.join(structured_lines)
    
    def apply_basic_formatting(self, content, font_size):
        """Apply basic accessibility formatting"""
        return f'<div style="font-size: {font_size}px; line-height: 1.6;">{content}</div>'
    
    # Visual content generation methods
    def generate_visual_content(self, subject, topic, content):
        """Generate visual content based on subject and topic"""
        subject_key = subject.lower()
        
        for key, visual_function in self.visual_templates.items():
            if key in subject_key:
                return visual_function(topic, content)
        
        return self.create_general_visual(topic, content)
    
    def create_math_visuals(self, topic, content):
        """Create mathematics-specific visuals"""
        if "addition" in topic.lower() or "arithmetic" in topic.lower():
            return self._create_addition_visual(content)
        elif "geometry" in topic.lower():
            return self._create_geometry_visual(content)
        elif "algebra" in topic.lower():
            return self._create_algebra_visual(content)
        else:
            return self._create_number_line_visual(content)
    
    def _create_addition_visual(self, content):
        """Create visual for addition problems"""
        # Extract numbers from content
        numbers = re.findall(r'\b\d+\b', content)
        if len(numbers) >= 2:
            num1, num2 = int(numbers[0]), int(numbers[1])
        else:
            num1, num2 = 15, 27  # Default numbers
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Visual 1: Block representation
        blocks1 = [1] * num1
        blocks2 = [2] * num2
        all_blocks = blocks1 + blocks2
        
        colors1 = ['lightblue'] * num1
        colors2 = ['lightcoral'] * num2
        all_colors = colors1 + colors2
        
        ax1.bar(range(len(all_blocks)), [1] * len(all_blocks), color=all_colors)
        ax1.set_title(f'Visual Addition: {num1} + {num2} = {num1 + num2}')
        ax1.set_xlabel('Total Items')
        ax1.set_ylabel('Count')
        ax1.text(0.5, 1.1, f'Blue: {num1}, Red: {num2}', 
                transform=ax1.transAxes, ha='center')
        
        # Visual 2: Number line
        ax2.plot([0, num1 + num2 + 5], [0, 0], 'k-', linewidth=2)
        for i in range(0, num1 + num2 + 1, 5):
            ax2.plot([i, i], [-0.1, 0.1], 'k-', linewidth=1)
            ax2.text(i, -0.3, str(i), ha='center')
        
        # Show the addition on number line
        ax2.arrow(num1, 0.2, num2, 0, head_width=0.1, head_length=0.5, 
                 fc='green', ec='green', length_includes_head=True)
        ax2.text(num1 + num2/2, 0.4, f'+{num2}', ha='center', color='green')
        
        ax2.set_title('Number Line Addition')
        ax2.set_xlim(-1, num1 + num2 + 5)
        ax2.set_ylim(-1, 1)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def _create_geometry_visual(self, content):
        """Create geometry visuals"""
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        
        # Square
        square = patches.Rectangle((1, 1), 3, 3, linewidth=2, 
                                 edgecolor='blue', facecolor='lightblue', alpha=0.7)
        ax1.add_patch(square)
        ax1.set_xlim(0, 5)
        ax1.set_ylim(0, 5)
        ax1.set_aspect('equal')
        ax1.set_title('Square\n4 equal sides\n4 right angles')
        
        # Circle
        circle = patches.Circle((2.5, 2.5), 2, linewidth=2, 
                              edgecolor='red', facecolor='lightcoral', alpha=0.7)
        ax2.add_patch(circle)
        ax2.set_xlim(0, 5)
        ax2.set_ylim(0, 5)
        ax2.set_aspect('equal')
        ax2.set_title('Circle\nNo corners\nConstant radius')
        
        # Triangle
        triangle = patches.Polygon([[1, 1], [4, 1], [2.5, 4]], linewidth=2,
                                 edgecolor='green', facecolor='lightgreen', alpha=0.7)
        ax3.add_patch(triangle)
        ax3.set_xlim(0, 5)
        ax3.set_ylim(0, 5)
        ax3.set_aspect('equal')
        ax3.set_title('Triangle\n3 sides\n3 angles')
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def _create_algebra_visual(self, content):
        """Create algebra equation visuals"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Simple linear equation visualization
        x = np.linspace(-5, 5, 100)
        y = 2*x + 1
        
        ax.plot(x, y, 'b-', linewidth=2, label='y = 2x + 1')
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('x values')
        ax.set_ylabel('y values')
        ax.set_title('Linear Equation: y = 2x + 1')
        ax.legend()
        
        # Mark key points
        ax.plot(-2, -3, 'ro', markersize=8, label='Points on the line')
        ax.plot(0, 1, 'ro', markersize=8)
        ax.plot(2, 5, 'ro', markersize=8)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def _create_number_line_visual(self, content):
        """Create general number line visual"""
        fig, ax = plt.subplots(figsize=(12, 3))
        
        # Create comprehensive number line
        ax.plot([-10, 10], [0, 0], 'k-', linewidth=3)
        
        # Major ticks
        for i in range(-10, 11, 2):
            ax.plot([i, i], [-0.2, 0.2], 'k-', linewidth=2)
            ax.text(i, -0.4, str(i), ha='center', fontsize=10)
        
        # Highlight positive and negative
        ax.axvspan(0, 10, alpha=0.2, color='green', label='Positive Numbers')
        ax.axvspan(-10, 0, alpha=0.2, color='red', label='Negative Numbers')
        
        ax.set_xlim(-11, 11)
        ax.set_ylim(-1, 1)
        ax.set_title('Number Line: Understanding Positive and Negative Numbers')
        ax.legend()
        ax.set_yticks([])
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def create_science_visuals(self, topic, content):
        """Create science-specific visuals"""
        if "biology" in topic.lower():
            return self._create_biology_visual(content)
        elif "physics" in topic.lower():
            return self._create_physics_visual(content)
        else:
            return self._create_science_general_visual(content)
    
    def _create_biology_visual(self, content):
        """Create biology cell structure visual"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Plant cell
        plant_cell = patches.Circle((0.5, 0.5), 0.4, linewidth=2, 
                                  edgecolor='green', facecolor='lightgreen', alpha=0.7)
        ax1.add_patch(plant_cell)
        
        # Cell parts
        ax1.add_patch(patches.Circle((0.5, 0.5), 0.1, facecolor='yellow', alpha=0.8))  # Nucleus
        ax1.add_patch(patches.Circle((0.3, 0.3), 0.05, facecolor='red', alpha=0.8))    # Chloroplast
        ax1.add_patch(patches.Rectangle((0.6, 0.6), 0.1, 0.1, facecolor='blue', alpha=0.6))  # Vacuole
        
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 1)
        ax1.set_aspect('equal')
        ax1.set_title('Plant Cell\n- Chloroplasts\n- Cell Wall\n- Large Vacuole')
        
        # Animal cell
        animal_cell = patches.Circle((0.5, 0.5), 0.4, linewidth=2, 
                                   edgecolor='red', facecolor='lightcoral', alpha=0.7)
        ax2.add_patch(animal_cell)
        
        # Cell parts
        ax2.add_patch(patches.Circle((0.5, 0.5), 0.15, facecolor='yellow', alpha=0.8))  # Nucleus
        ax2.add_patch(patches.Circle((0.3, 0.6), 0.06, facecolor='purple', alpha=0.8))  # Mitochondria
        ax2.add_patch(patches.Rectangle((0.6, 0.3), 0.08, 0.08, facecolor='orange', alpha=0.6))  # Lysosome
        
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 1)
        ax2.set_aspect('equal')
        ax2.set_title('Animal Cell\n- Multiple Small Vacuoles\n- No Cell Wall\n- Various Organelles')
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def _create_physics_visual(self, content):
        """Create physics visuals"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Simple physics concept - forces
        ax.arrow(1, 1, 2, 0, head_width=0.2, head_length=0.3, fc='blue', ec='blue', label='Applied Force')
        ax.arrow(3, 1, -1, 0, head_width=0.2, head_length=0.3, fc='red', ec='red', label='Friction')
        ax.arrow(2, 1, 0, 1, head_width=0.2, head_length=0.3, fc='green', ec='green', label='Normal Force')
        ax.arrow(2, 1, 0, -0.5, head_width=0.2, head_length=0.3, fc='orange', ec='orange', label='Gravity')
        
        ax.set_xlim(0, 5)
        ax.set_ylim(0, 3)
        ax.set_aspect('equal')
        ax.set_title('Forces Acting on an Object')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def _create_science_general_visual(self, content):
        """Create general science visual"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Scientific method flowchart
        steps = ['Observation', 'Question', 'Hypothesis', 'Experiment', 'Analysis', 'Conclusion']
        colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightcoral', 'lightpurple', 'lightgray']
        
        for i, (step, color) in enumerate(zip(steps, colors)):
            ax.add_patch(patches.Rectangle((1, i), 3, 0.8, facecolor=color, alpha=0.7, edgecolor='black'))
            ax.text(2.5, i + 0.4, step, ha='center', va='center', fontsize=12, weight='bold')
            if i < len(steps) - 1:
                ax.arrow(2.5, i + 0.8, 0, 0.2, head_width=0.1, head_length=0.1, fc='black')
        
        ax.set_xlim(0, 5)
        ax.set_ylim(-0.5, len(steps) + 0.5)
        ax.set_aspect('equal')
        ax.set_title('Scientific Method Process')
        ax.set_xticks([])
        ax.set_yticks([])
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def create_language_visuals(self, topic, content):
        """Create language arts visuals"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Sentence structure visualization
        sentences = [
            "The quick brown fox jumps over the lazy dog.",
            "She read the interesting book quietly in the library.",
            "After the rain stopped, children played in the puddles."
        ]
        
        # Color code parts of speech (simplified)
        colors = {'noun': 'lightblue', 'verb': 'lightcoral', 
                 'adjective': 'lightgreen', 'other': 'lightyellow'}
        
        y_pos = 0
        for sentence in sentences:
            words = sentence.split()
            x_pos = 0
            
            for word in words:
                # Simple word type classification (in real app, use NLP)
                if len(word) <= 3:
                    color = colors['other']
                elif word.endswith('ed') or word.endswith('ing'):
                    color = colors['verb']
                elif word in ['quick', 'brown', 'lazy', 'interesting', 'quiet']:
                    color = colors['adjective']
                else:
                    color = colors['noun']
                
                ax.add_patch(patches.Rectangle((x_pos, y_pos), len(word)*0.5, 0.8, 
                                             facecolor=color, alpha=0.7, edgecolor='black'))
                ax.text(x_pos + len(word)*0.25, y_pos + 0.4, word, 
                       ha='center', va='center', fontsize=8)
                x_pos += len(word)*0.5 + 0.2
            
            y_pos += 1.2
        
        ax.set_xlim(0, 20)
        ax.set_ylim(0, y_pos)
        ax.set_title('Sentence Structure Visualization\n\nColors show different word types')
        
        # Legend
        legend_elements = [
            patches.Patch(facecolor=colors['noun'], label='Nouns', alpha=0.7),
            patches.Patch(facecolor=colors['verb'], label='Verbs', alpha=0.7),
            patches.Patch(facecolor=colors['adjective'], label='Adjectives', alpha=0.7),
            patches.Patch(facecolor=colors['other'], label='Other Words', alpha=0.7)
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        ax.set_aspect('equal')
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def create_history_visuals(self, topic, content):
        """Create history timeline visual"""
        fig, ax = plt.subplots(figsize=(12, 4))
        
        # Sample timeline events
        events = [
            ("3000 BCE", "Early Civilizations"),
            ("500 BCE", "Classical Age"),
            ("500 CE", "Middle Ages"),
            ("1500 CE", "Renaissance"),
            ("1800 CE", "Industrial Revolution"),
            ("2000 CE", "Modern Era")
        ]
        
        # Convert years to numeric for plotting
        years = []
        for year_str, _ in events:
            if 'BCE' in year_str:
                year = -int(year_str.replace(' BCE', ''))
            else:
                year = int(year_str.replace(' CE', ''))
            years.append(year)
        
        # Create timeline
        ax.plot(years, [0] * len(years), 'o-', linewidth=3, markersize=8)
        
        for i, ((year_str, event), year) in enumerate(zip(events, years)):
            ax.annotate(f"{year_str}\n{event}", (year, 0), 
                       xytext=(0, 20 if i % 2 == 0 else -30), 
                       textcoords='offset points', 
                       ha='center', va='bottom' if i % 2 == 0 else 'top',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7),
                       arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0"))
        
        ax.set_xlim(min(years) - 500, max(years) + 500)
        ax.set_ylim(-1, 1)
        ax.set_title('Historical Timeline')
        ax.set_yticks([])
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def create_general_visual(self, topic, content):
        """Create a general concept map visual"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Simple concept map
        concepts = [topic, "Key Idea 1", "Key Idea 2", "Key Idea 3", "Example", "Application"]
        positions = [(0.5, 0.8), (0.2, 0.5), (0.5, 0.5), (0.8, 0.5), (0.3, 0.2), (0.7, 0.2)]
        
        for (concept, (x, y)) in zip(concepts, positions):
            ax.add_patch(patches.Circle((x, y), 0.08, facecolor='lightblue', alpha=0.7, edgecolor='black'))
            ax.text(x, y, concept, ha='center', va='center', fontsize=8, wrap=True)
        
        # Connect concepts
        connections = [(0, 1), (0, 2), (0, 3), (1, 4), (2, 5), (3, 5)]
        for i, j in connections:
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            ax.plot([x1, x2], [y1, y2], 'k-', alpha=0.5)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.set_title(f'Concept Map: {topic}')
        ax.set_xticks([])
        ax.set_yticks([])
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def _fig_to_base64(self, fig):
        """Convert matplotlib figure to base64 string for Streamlit"""
        try:
            buf = BytesIO()
            fig.savefig(buf, format="png", dpi=150, bbox_inches='tight')
            buf.seek(0)
            img_str = base64.b64encode(buf.read()).decode()
            plt.close(fig)  # Close the figure to free memory
            return img_str
        except Exception as e:
            print(f"Error creating figure: {e}")
            return None