
import os

os.makedirs("cards", exist_ok=True)

svg = """
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="250">

    <style>
        .hello {
            animation: fadeIn 1s ease forwards;
        }

        .name {
            animation: slideUp 1.5s ease forwards;
        }

        .subtitle {
            animation: fadeIn 2.5s ease forwards;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>

    <rect width="100%" height="100%" fill="#F5F1E8"/>

    <text x="50" y="90" font-size="24"
          fill="#2563EB" class="hello">
        HELLO, I'M
    </text>

    <text x="50" y="155" font-size="55"
          font-weight="bold" fill="#222222"
          class="name">
        VIVEK BHAMARE
    </text>

    <text x="50" y="200" font-size="20"
          fill="#555555" class="subtitle">
        BCA Student | Aspiring Data Scientist
    </text>

</svg>
"""

with open("cards/hero.svg", "w", encoding="utf-8") as file:
    file.write(svg)

print("Animated Hero Card generated successfully!")
