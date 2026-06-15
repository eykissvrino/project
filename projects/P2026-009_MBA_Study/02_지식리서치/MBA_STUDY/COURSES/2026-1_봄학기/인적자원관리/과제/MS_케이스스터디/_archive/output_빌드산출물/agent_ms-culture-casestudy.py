#!/usr/bin/env python3
"""
Microsoft Case Study - Satya Nadella Growth Mindset
MBA 인적자원관리 발표 덱 (23 slides)
"""

import sys, os
sys.path.insert(0, os.path.expanduser("C:/Users/eykis/.claude/plugins/mckinsey-pptx"))

from dataclasses import replace
from mckinsey_pptx import PresentationBuilder, DEFAULT_THEME
from mckinsey_pptx.theme import Typography

# Windows Korean theme: Malgun Gothic
KO_THEME = replace(
    DEFAULT_THEME,
    typography=replace(DEFAULT_THEME.typography, family="Malgun Gothic"),
    copyright_text="\u24d2 2026 MBA HRM",
)

b = PresentationBuilder(theme=KO_THEME, default_section_marker="MS Culture Case")

# ── Slide 1: Cover ──────────────────────────────────────────
b.add("cover_slide",
      title="Microsoft Case Study",
      subtitle="Satya Nadella at Microsoft:\nInstilling a Growth Mindset",
      client="MBA HRM | LBS128 (2018)",
      date="2026. 5. 16.")

# ── Slide 2: Agenda ─────────────────────────────────────────
b.add("agenda",
      title="Agenda",
      items=[
          "Executive Summary",
          "PART 1 \u2014 \ucf00\uc774\uc2a4 \ubc30\uacbd: \uc783\uc5b4\ubc84\ub9b0 10\ub144",
          "PART 2 \u2014 As-Is \uc9c4\ub2e8: 7S \uc870\uc9c1 \ubcd1\ub9ac",
          "PART 3 \u2014 \ubcc0\ud654\uc758 \ub3d9\uc778: Nadella",
          "PART 4 \u2014 To-Be: Growth Mindset \uc870\uc9c1",
          "PART 5 \u2014 \uc2e4\ud589 \uba54\ucee4\ub2c8\uc998: Kotter + Schein",
          "PART 6 \u2014 \uc131\uacfc \u00b7 \uc2dc\uc0ac\uc810 \u00b7 \ud1a0\ub860",
      ])

# ── Slide 3: Dark Navy Impact ───────────────────────────────
b.add("dark_navy_summary",
      body='[Core Thesis]: Nadella\ub294 \uc804\ub7b5\uc774 \uc544\ub2cc "\uc778\uac04 \uc2dc\uc2a4\ud15c"\uc744 \ubcc0\ud601\uc758 \ucd9c\ubc1c\uc810\uc73c\ub85c \uc0bc\uc558\ub2e4 \u2014 "CEO\uc758 C\ub294 Culture\uc758 \uc57d\uc790\ub2e4"',
      eyebrow="Microsoft Case Study")

# ── Slide 4: Executive Summary ──────────────────────────────
b.add("executive_summary_takeaways",
      title="\ud575\uc2ec \uc778\uc0ac\uc774\ud2b8 \uc694\uc57d",
      sections=[
          {"takeaway": "\uc131\uacfc\uad00\ub9ac \uc2dc\uc2a4\ud15c\uc740 \ubb38\ud654\uc758 DNA\ub2e4",
           "bullets": [
               "Stack Ranking\uc774 \ub0b4\ubd80 \uacbd\uc7c1\u00b7\uc815\uce58\u00b7\uc704\ud5d8\ud68c\ud53c \ud589\ub3d9\uc744 \uc124\uacc4",
               "\ud3d0\uc9c0 \ud6c4 \uc0c1\uc2dc \ud53c\ub4dc\ubc31\uc73c\ub85c \uc804\ud658 \u2192 \ud611\uc5c5 \ud68c\ubcf5",
           ]},
          {"takeaway": "\ubb38\ud654 \ubcc0\ud601 = \ub9d0 + \uc81c\ub3c4 + \ud589\ub3d9 + \ud658\uacbd\uc758 \uc815\ud569\uc131",
           "bullets": [
               "\uc0c8 \ubbf8\uc158(\ub9d0) + Stack Ranking \ud3d0\uc9c0(\uc81c\ub3c4) + CEO \uc194\uc120\uc218\ubc94(\ud589\ub3d9) + \ub123\uc9c0(\ud658\uacbd)",
               "7S \uc694\uc18c\ub97c Cloud\u00b7Empowerment \ucd95\uc73c\ub85c \ub3d9\uc2dc \uc7ac\uc815\ub82c",
           ]},
          {"takeaway": "\uacf5\uac10(Empathy)\uc740 \uc804\ub7b5\uc801 \uc5ed\ub7c9\uc774\ub2e4",
           "bullets": [
               "Nadella\uc758 \uac1c\uc778 \uacbd\ud5d8(\uc7a5\ub0a8 Zain) \u2192 \uc870\uc9c1 \uc804\uccb4\uc758 \uacf5\uac10 \ubb38\ud654",
               "\ucde8\uc57d\uc131(Vulnerability) \uacf5\uac1c\ub85c Growth Mindset \uc804\ud30c",
           ]},
          {"takeaway": "\ucd5c\ub300 \ub9ac\uc2a4\ud06c: '\uc0c8\ub85c\uc6b4 \uc5b8\uc5b4, \uc624\ub798\ub41c \ud589\ub3d9'",
           "bullets": [
               "Missing Middle \u2014 \uc911\uac04\uad00\ub9ac\uc790 \uce35\uc758 \ubcc0\ud654 \uc800\ud56d",
               "\ubb38\ud654 \uc5b8\uc5b4\uac00 \uc815\uce58 \ud589\ub3d9\uc744 \ud3ec\uc7a5\ud558\ub294 \ub3c4\uad6c\ub85c \uc804\ub77d \uc704\ud5d8",
           ]},
      ],
      final_conclusion="\uc804\ub7b5\u00b7\uad6c\uc870\u00b7\ubb38\ud654\u00b7\uc81c\ub3c4\uc758 \uc815\ud569\uc131\uc774 \uc870\uc9c1 \ud6a8\uacfc\uc131\uc744 \uacb0\uc815\ud55c\ub2e4")

# ── Slide 5: Section Divider - PART 1 ───────────────────────
b.add("section_divider",
      section_number="01",
      section_title="\ucf00\uc774\uc2a4 \ubc30\uacbd",
      subtitle="\uc783\uc5b4\ubc84\ub9b0 10\ub144\uc758 \uc5ed\uc124")

# ── Slide 6: KPI Dashboard - Lost Decade ────────────────────
b.add("kpi_dashboard",
      title="\uc783\uc5b4\ubc84\ub9b0 10\ub144: \uc7ac\ubb34\ub294 \uba40\uca61\ud55c\ub370 \uc2dc\uc7a5\uc740 \ubd88\uc2e0",
      kpis=[
          {"label": "\ub9e4\ucd9c \uc131\uc7a5", "value": "3\ubc30",
           "delta": "2000\u219214", "delta_dir": "up",
           "context": "Ballmer \uc7ac\uc784\uae30 \ub9e4\ucd9c"},
          {"label": "\uc774\uc775 \uc131\uc7a5", "value": "2\ubc30",
           "delta": "2000\u219214", "delta_dir": "up",
           "context": "\uc601\uc5c5\uc774\uc775 \uae30\uc900"},
          {"label": "\uc8fc\uac00", "value": "\uc815\uccb4",
           "delta": "10\ub144\uac04 \ud69f\ubcf4", "delta_dir": "down",
           "context": "\uc2dc\uc7a5\uc740 \ubbf8\ub798 \uc131\uc7a5\uc744 \ubd88\uc2e0"},
          {"label": "CEO \uc9c0\uc9c0\uc728", "value": "29%",
           "delta": "Ballmer (2011)", "delta_dir": "down",
           "context": "Larry Page 94%, Zuckerberg 99%"},
          {"label": "\ud575\uc2ec \uc778\uc7ac", "value": "\uc720\ucd9c",
           "delta": "2004\ub144\ubd80\ud130", "delta_dir": "down",
           "context": "Google \ub4f1\uc73c\ub85c \uc774\ud0c8 \uac00\uc18d"},
          {"label": "\uc2dc\uc7a5 \uc120\uc810", "value": "\uc2e4\ud328",
           "delta": "e-book, \uc2a4\ub9c8\ud2b8\ud3f0", "delta_dir": "down",
           "context": "bickering\uacfc power plays\ub85c \uc0c1\uc2e4"},
      ],
      columns=3)

# ── Slide 7: Quote ───────────────────────────────────────────
b.add("quote_slide",
      title="\uc783\uc5b4\ubc84\ub9b0 \uc601\ud63c",
      quote="\uad00\ub8cc\uc8fc\uc758\uac00 \ud601\uc2e0\uc744 \ub300\uccb4\ud588\uace0, \uc0ac\ub0b4 \uc815\uce58\uac00 \ud300\uc6cc\ud06c\ub97c \ub300\uc2e0\ud588\ub2e4. \uc6b0\ub9ac\ub294 \ub099\uc624\ud588\ub2e4.",
      author="Satya Nadella",
      author_title="Hit Refresh (2018), p.19")

# ── Slide 8: Section Divider - PART 2 ───────────────────────
b.add("section_divider",
      section_number="02",
      section_title="As-Is \uc9c4\ub2e8",
      subtitle="Ballmer \uc2dc\ub300\uc758 7S \uc870\uc9c1 \ubcd1\ub9ac")

# ── Slide 9: 7S As-Is - Overview Areas (7 items) ────────────
b.add("overview_areas",
      title="7S \ubaa8\ub378 As-Is \uc9c4\ub2e8: 7\uc694\uc18c \ubd80\uc815\ud569",
      areas=[
          {"name": "Strategy",
           "bullets": ["Windows \ubc29\uc5b4 \uc911\uc2ec", "\ubaa8\ubc14\uc77c\u00b7\ud074\ub77c\uc6b0\ub4dc \uc804\ud658 \uc2e4\ud328"]},
          {"name": "Structure",
           "bullets": ["\uc81c\ud488\ubcc4 \uc0ac\uc77c\ub85c", "\ubd09\uac74 \uc601\uc8fc\uad6d\uc758 \uc5f0\ud569"]},
          {"name": "Systems",
           "bullets": ["Stack Ranking", "6\uac1c\uc6d4 \uac15\uc81c \uc11c\uc5f4\ud654"]},
          {"name": "Style",
           "bullets": ["\uacf5\uaca9\uc801 \uac80\uc99d \ubb38\ud654", "\uc704\uacc4\uc801\u00b7\ud615\uc2dd\uc801"]},
          {"name": "Staff",
           "bullets": ["\uc815\uce58\uc801 \uc0dd\uc874\uc790 \uc704\uc8fc", "\uc778\uc7ac \uc720\ucd9c \uc9c0\uc18d"]},
          {"name": "Skills",
           "bullets": ["PC SW \uc5ed\ub7c9 \uace0\ucc29", "\ud074\ub77c\uc6b0\ub4dc\u00b7\uc624\ud508\uc18c\uc2a4 \ubd80\uc7ac"]},
          {"name": "Shared Values",
           "bullets": ["Know-it-all", "\uac00\uc7a5 \ub611\ub611\ud568\uc744 \uc99d\uba85\ud558\ub77c"]},
      ],
      call_out="PC \uc2dc\ub300\uc758 \ubc29\uc5b4\ub85c \uc815\ub82c\ub41c \uc545\uc21c\ud658",
      source="McKinsey 7S Framework / LBS128 Case")

# ── Slide 10: Stack Ranking Before/After ─────────────────────
b.add("two_column_compare",
      title="Stack Ranking \u2192 \uc0c1\uc2dc \ud53c\ub4dc\ubc31",
      left_label="As-Is: Stack Ranking",
      right_label="To-Be: Continuous Feedback",
      left_items=[
          "6\uac1c\uc6d4 \uac15\uc81c \uc11c\uc5f4\ud654",
          "\uc0c1\ub300\ud3c9\uac00 (10\uba85 \uc911 1\uba85 \u5fc5 poor)",
          "\uc54c\uace0\ub9ac\uc998 \ub4f1\uae09 \uc5f0\ub3d9 \ubcf4\uc0c1",
          "\ubaa9\uc801: \ubd84\ub958\uc640 \ub3c4\ud0dc",
      ],
      right_items=[
          "\uc0c1\uc2dc \ud53c\ub4dc\ubc31\u00b7\ucf54\uce6d",
          "\uc808\ub300\uc801 \uae30\uc5ec\ub3c4 + \uc131\uc7a5",
          "\ub9e4\ub2c8\uc800 \uc7ac\ub7c9 \ubcf4\uc0c1 \uc608\uc0b0",
          "\ubaa9\uc801: \uc131\uc7a5\uacfc \uac1c\ubc1c",
      ],
      left_color="navy",
      right_color="blue")

# ── Slide 11: 3 Destruction Mechanisms ───────────────────────
b.add("three_trends_icons",
      title="Stack Ranking\uc758 3\ub300 \ud30c\uad34 \uba54\ucee4\ub2c8\uc998",
      trends=[
          {"label": "\ud611\uc5c5 \ud30c\uad34",
           "icon": "\u2694",
           "bullets": [
               "\ub3d9\ub8cc\uc758 \uc2e4\ud328 = \ub098\uc758 \uc0c1\ub300\uc801 \uc131\uacf5",
               "\uc81c\ub85c\uc12c \uac8c\uc784\uc73c\ub85c \ud611\uc5c5 \ubd88\uac00",
           ]},
          {"label": "\uc815\uce58 \uc81c\ub3c4\ud654",
           "icon": "\u2666",
           "bullets": [
               "\uc815\uce58 \uc548 \ud558\uba74 character assassination",
               "\uacbd\ub825 \uac1c\ubc1c\uc758 \ud575\uc2ec\uc774 \uc815\uce58 \uac8c\uc784",
           ]},
          {"label": "\ud601\uc2e0 \uc5b5\uc555",
           "icon": "\u2716",
           "bullets": [
               "designing software by committee",
               "\uc758\uc0ac\uacb0\uc815\uc758 \uad00\ub8cc\ud654",
           ]},
      ],
      source="Vanity Fair (2012) / LBS128 Case")

# ── Slide 12: Section Divider - PART 3 ──────────────────────
b.add("section_divider",
      section_number="03",
      section_title="\ubcc0\ud654\uc758 \ub3d9\uc778",
      subtitle="Satya Nadella \u2014 \ub0b4\ubd80\uc790\uc758 \uc678\ubd80 \uc2dc\uc120")

# ── Slide 13: Nadella Profile - 5 Key Areas ─────────────────
b.add("five_key_areas",
      title="Nadella\uac00 \ubcc0\ud601\uc744 \uc774\ub04c \uc218 \uc788\uc5c8\ub358 5\uac00\uc9c0 \uc694\uc778",
      areas=[
          {"name": "22\ub144 \ub0b4\ubd80\uc790",
           "description": "1992\ub144 \uc785\uc0ac, Cloud & Enterprise EVP \ucd9c\uc2e0"},
          {"name": "\ud559\uc2b5 \uc9c0\ud5a5 \uacbd\ub825",
           "description": "Bing \ub4f1 \ub9ac\uc2a4\ud06c \ubcf4\uc9c1 \uc790\ubc1c \uc218\ud589"},
          {"name": "\uacf5\uac10\uc758 \uccb4\ud654",
           "description": "\uc7a5\ub0a8 Zain\uc758 \ub1cc\uc131\ub9c8\ube44 \u2192 Empathy \ub9ac\ub354\uc2ed"},
          {"name": "Growth Mindset",
           "description": "Carol Dweck Mindset \u2014 \uc544\ub0b4 Anu\uc758 \ucd94\ucc9c"},
          {"name": "\uacbd\uccad\uc758 1\ub144",
           "description": "\ubaa8\ub4e0 \ub808\ubca8 \uc218\ubc31 \uba85 \uc778\ud130\ubdf0, '\uc65c MS\uac00 \uc874\uc7ac\ud558\ub294\uac00?'"},
      ])

# ── Slide 14: Section Divider - PART 4 ──────────────────────
b.add("section_divider",
      section_number="04",
      section_title="To-Be \uc7ac\uc124\uacc4",
      subtitle="Growth Mindset \uc870\uc9c1\uc73c\ub85c\uc758 \uc804\ud658")

# ── Slide 15: Fixed vs Growth Mindset Comparison ─────────────
b.add("comparison_table",
      title="Fixed Mindset vs Growth Mindset",
      subtitle="Carol Dweck (2006) \u2192 Microsoft \uc870\uc9c1 \uc801\uc6a9",
      options=["Fixed (As-Is)", "Growth (To-Be)"],
      criteria=[
          {"name": "\ud575\uc2ec \uc2e0\ub150",
           "scores": ["low", "high"],
           "notes": ["\ub2a5\ub825\uc740 \uace0\uc815\uc801", "\ub2a5\ub825\uc740 \uc131\uc7a5 \uac00\ub2a5"]},
          {"name": "\uc2e4\ud328 \ub300\uc751",
           "scores": ["low", "high"],
           "notes": ["\ud68c\ud53c\u00b7\uc740\ud3d0\u00b7\ub0a8 \ud0d3", "\ud559\uc2b5 \uae30\ud68c\ub85c \ud65c\uc6a9"]},
          {"name": "\ub3c4\uc804 \ud0dc\ub3c4",
           "scores": ["low", "high"],
           "notes": ["\uc775\uc219\ud55c \uac83\ub9cc \uace0\uc218", "\uc0c8\ub85c\uc6b4 \ub3c4\uc804 \ucd94\uad6c"]},
          {"name": "\ud0c0\uc778\uc758 \uc131\uacf5",
           "scores": ["low", "high"],
           "notes": ["\uc704\ud611\uc73c\ub85c \uc778\uc2dd", "\uc601\uac10\uc758 \uc6d0\ucc9c"]},
          {"name": "\uc870\uc9c1 \uc801\uc6a9",
           "scores": ["low", "high"],
           "notes": ["Know-it-all", "Learn-it-all"]},
      ],
      recommended_index=1)

# ── Slide 16: 3 Pillars ─────────────────────────────────────
b.add("three_trends_icons",
      title="Growth Mindset 3\ub300 Pillar",
      subtitle="Kathleen Hogan CPO \uc8fc\ub3c4, Culture Cabinet, Carol Dweck \uc790\ubb38",
      trends=[
          {"label": "Customer Obsession",
           "icon": "\u2605",
           "bullets": [
               "\uace0\uac1d\uc758 \ubbf8\ucda9\uc871 \ub2c8\uc988\uc5d0 \ud638\uae30\uc2ec\uacfc \uacbd\uccad",
               "\uc624\uc2a4\ud2b8\ub9ac\uc544 GM: \uacbd\ucc30\uc11c\u00b7\ubcd1\uc6d0 \ud604\uc7a5 \uad00\ucc30",
           ]},
          {"label": "Diversity & Inclusion",
           "icon": "\u2660",
           "bullets": [
               "\uc9c0\uad6c\ub97c \uc12c\uae30\ub824\uba74 \uc9c0\uad6c\ub97c \ubc18\uc601\ud558\ub77c",
               "\ub2e4\uc591\uc131 \ubaa9\ud45c \uc218\uce58\ud654, \ubcf4\ub108\uc2a4 \uc5f0\uacc4",
           ]},
          {"label": "One Microsoft",
           "icon": "\u2726",
           "bullets": [
               "\ubd09\uac74 \uc601\uc8fc\uad6d \u2192 \ud558\ub098\uc758 \ud68c\uc0ac",
               "OneWeek \ud574\ucee4\ud1a4: \ubd80\uc11c \ud6a1\ub2e8 \ud300",
           ]},
      ])

# ── Slide 17: CVF Matrix - Prioritization ───────────────────
b.add("prioritization_matrix",
      title="\uacbd\uc7c1\uac00\uce58\ubaa8\ud615: \ubb38\ud654 \uc720\ud615 \uc804\ud658",
      items=[
          # As-Is (amber/red) in Hierarchy + Market
          {"name": "Hierarchy\n(\uc704\uacc4)",
           "x_band": 0, "y_band": 2, "status": "red"},
          {"name": "Market\n(\uacbd\uc7c1)",
           "x_band": 2, "y_band": 2, "status": "red"},
          # To-Be (green) in Clan + Adhocracy
          {"name": "Clan\n(\ud611\ub825)",
           "x_band": 0, "y_band": 0, "status": "green"},
          {"name": "Adhocracy\n(\ud601\uc2e0)",
           "x_band": 2, "y_band": 0, "status": "green"},
      ],
      source="Cameron & Quinn \uacbd\uc7c1\uac00\uce58\ubaa8\ud615 (CVF)")

# ── Slide 18: Section Divider - PART 5 ──────────────────────
b.add("section_divider",
      section_number="05",
      section_title="\uc2e4\ud589 \uba54\ucee4\ub2c8\uc998",
      subtitle="12.5\ub9cc \uba85\uc744 \uc5b4\ub5bb\uac8c \uc6c0\uc9c1\uc600\ub294\uac00")

# ── Slide 19: Kotter 8 Steps - Process Flow ─────────────────
b.add("process_flow_horizontal",
      title="Kotter 8\ub2e8\uacc4 \u00d7 Nadella \ud589\ubcf4",
      steps=[
          {"name": "\uc704\uae30\uac10 \uc870\uc131",
           "description": "\uc783\uc5b4\ubc84\ub9b0 10\ub144 \uc9c1\uc2dc"},
          {"name": "\ucd94\uc9c4 \uc5f0\ud569",
           "description": "SLT + Culture Cabinet"},
          {"name": "\ube44\uc804 \uc218\ub9bd",
           "description": "\uc0c8 \ubbf8\uc158 + 3 Pillar"},
          {"name": "\ube44\uc804 \uc804\ud30c",
           "description": "\uc6d4\uac04 \uc601\uc0c1 + Hit Refresh"},
          {"name": "\uc7a5\uc560 \uc81c\uac70",
           "description": "Stack Ranking \ud3d0\uc9c0"},
          {"name": "\ub2e8\uae30 \uc131\uacfc",
           "description": "Office on iOS, Linux"},
      ],
      source="Kotter (1996) 8-Step Change Model")

# ── Slide 20: Schein 3 Levels ───────────────────────────────
b.add("three_trends_table",
      title="Schein \ubb38\ud654 3\uc218\uc900 \ubcc0\ud601 \ub9e4\ud551",
      trends=[
          {"name": "Artifacts",
           "description": [
               "As-Is: Stack Ranking \uc591\uc2dd",
               "As-Is: \uacf5\uaca9\uc801 \ud68c\uc758 \ubb38\ud654",
           ],
           "examples": [
               "\uc0c1\uc2dc \ud53c\ub4dc\ubc31 \ub3c4\uc785",
               "\ud574\ucee4\ud1a4\u00b7\ub123\uc9c0 \ub3c4\uc785",
           ]},
          {"name": "Espoused Values",
           "description": [
               "As-Is: \ub611\ub611\ud55c \uc790\uac00 \uc774\uae34\ub2e4",
               "To-Be: Growth Mindset",
           ],
           "examples": [
               "\uc0c8 \ubbf8\uc158 \uc120\uc5b8",
               "Hit Refresh \uc804 \uc9c1\uc6d0 \ubc30\ud3ec",
           ]},
          {"name": "Basic Assumptions",
           "description": [
               "As-Is: \ub2a5\ub825\uc740 \uace0\uc815, \uacbd\uc7c1=\uc131\uacfc",
               "To-Be: \uc131\uc7a5 \uac00\ub2a5, \ud559\uc2b5=\uc131\uacfc",
           ],
           "examples": [
               "CEO Role Modeling",
               "\ucde8\uc57d\uc131 \uacf5\uac1c\ub85c \uc2e0\ub8b0 \uad6c\ucd95",
           ]},
      ],
      source="Edgar Schein, Organizational Culture & Leadership")

# ── Slide 21: Section Divider - PART 6 ──────────────────────
b.add("section_divider",
      section_number="06",
      section_title="\uc131\uacfc \u00b7 \uc2dc\uc0ac\uc810 \u00b7 \ud1a0\ub860",
      subtitle="4\ub144\uc758 \uc131\uacfc\uc640 \ubbf8\ud574\uacb0 \uacfc\uc81c")

# ── Slide 22: KPI Dashboard - 4-Year Results ────────────────
b.add("kpi_dashboard",
      title="Nadella 4\ub144\ucc28 \uc131\uacfc (2018)",
      kpis=[
          {"label": "\uc2dc\uac00\ucd1d\uc561", "value": "$700B",
           "delta": "\uc0ac\uc0c1 \ucd5c\uace0", "delta_dir": "up",
           "context": "\uc8fc\uac00 \uc815\uccb4 \u2192 \uae09\ub4f1"},
          {"label": "Azure \uc810\uc720", "value": "95%+",
           "delta": "Fortune 500 \uc0ac\uc6a9", "delta_dir": "up",
           "context": "\uae00\ub85c\ubc8c 50\uac1c \ub9ac\uc804 \ubc1c\ud45c"},
          {"label": "CEO \uc9c0\uc9c0\uc728", "value": "95%",
           "delta": "29% \u2192 95%", "delta_dir": "up",
           "context": "Glassdoor \uae30\uc900"},
          {"label": "\uc778\uc7ac \ud750\ub984", "value": "Top 5 AI",
           "delta": "\uc720\ucd9c \u2192 \uc720\uc785", "delta_dir": "up",
           "context": "\ucd5c\uace0 \uc5d4\uc9c0\ub2c8\uc5b4 \uc778\uc7ac\uc758 \uc790\uc11d"},
          {"label": "\uc678\ubd80 \uad00\uacc4", "value": "Open",
           "delta": "Linux \ud3ec\uc6a9", "delta_dir": "up",
           "context": "cancer \u2192 \ud30c\ud2b8\ub108\uc2ed"},
          {"label": "M&A", "value": "$26B",
           "delta": "LinkedIn \uc778\uc218", "delta_dir": "up",
           "context": "\uc0dd\ud0dc\uacc4 \ud655\uc7a5 \uc804\ub7b5"},
      ],
      columns=3)

# ── Slide 23: Key Insights + Discussion ──────────────────────
b.add("five_key_areas",
      title="\ud575\uc2ec \uc778\uc0ac\uc774\ud2b8 5 + \ud1a0\ub860 \uc8fc\uc81c",
      areas=[
          {"name": "\uc131\uacfc\uad00\ub9ac = \ubb38\ud654 DNA",
           "description": "Stack Ranking\uc774 \ud589\ub3d9\uc744 \uc124\uacc4\ud588\ub2e4"},
          {"name": "\uc815\ud569\uc131\uc774 \ud575\uc2ec",
           "description": "\ub9d0+\uc81c\ub3c4+\ud589\ub3d9+\ud658\uacbd\uc758 \ub3d9\uc2dc \uc791\ub3d9"},
          {"name": "\uacf5\uac10 = \uc804\ub7b5\uc801 \uc5ed\ub7c9",
           "description": "Empathy\ub294 \uc18c\ud504\ud2b8 \uc2a4\ud0ac\uc774 \uc544\ub2c8\ub2e4"},
          {"name": "\ucde8\uc57d\uc131\uc774 \uc2e0\ub8b0\ub97c \uad6c\ucd95",
           "description": "Grace Hopper + Tay \uc0ac\uac74\uc758 \uad50\ud6c8"},
          {"name": "\uc0c8 \uc5b8\uc5b4, \uc624\ub798\ub41c \ud589\ub3d9",
           "description": "\ubb38\ud654 \uc5b8\uc5b4\uac00 \uc815\uce58 \ub3c4\uad6c\ub85c \uc804\ub77d \uc704\ud5d8"},
      ],
      source="\ud1a0\ub860: Stack Ranking \ub9e5\ub77d | Growth Mindset \uad6c\ud638\ud654 | CEO \uc758\uc874\uc131 | \ud55c\uad6d \uc801\uc6a9")

# ── Save ─────────────────────────────────────────────────────
output_dir = r"C:\Users\eykis\OneDrive\vrin_AI_hub\projects\P2026-009_MBA_Study\MBA_STUDY\인적자원관리_과제_MS 케이스스터디\output"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "ms-culture-casestudy.pptx")
b.save(output_path)
print(f"Saved: {output_path}")
