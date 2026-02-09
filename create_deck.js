const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const {
  FaRocket, FaSearch, FaClipboardList, FaPenFancy,
  FaCloudUploadAlt, FaBook, FaCode, FaMagic,
  FaCogs, FaFileAlt, FaTerminal, FaBolt,
  FaCheckCircle, FaArrowRight
} = require("react-icons/fa");

function renderIconSvg(IconComponent, color = "#000000", size = 256) {
  return ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size: String(size) })
  );
}

async function iconToBase64Png(IconComponent, color, size = 256) {
  const svg = renderIconSvg(IconComponent, color, size);
  const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}

// --- Color palette: Teal Trust ---
const C = {
  dark:    "0B1D26",   // near-black teal
  primary: "028090",   // teal
  mid:     "00A896",   // seafoam
  accent:  "02C39A",   // mint
  light:   "F0FAF8",   // very light mint
  white:   "FFFFFF",
  text:    "1A2E35",   // dark text
  muted:   "5A7A85",   // muted text
  card:    "E8F5F2",   // card bg
};

const makeShadow = () => ({
  type: "outer", blur: 8, offset: 2, angle: 135,
  color: "000000", opacity: 0.10
});

async function main() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.author = "ReadMe Hackathon Team";
  pres.title = "generate-docs — Hackathon Pitch";

  // Pre-render icons
  const icons = {
    rocket:    await iconToBase64Png(FaRocket, `#${C.white}`),
    search:    await iconToBase64Png(FaSearch, `#${C.primary}`),
    clipboard: await iconToBase64Png(FaClipboardList, `#${C.primary}`),
    pen:       await iconToBase64Png(FaPenFancy, `#${C.primary}`),
    upload:    await iconToBase64Png(FaCloudUploadAlt, `#${C.primary}`),
    book:      await iconToBase64Png(FaBook, `#${C.white}`),
    code:      await iconToBase64Png(FaCode, `#${C.white}`),
    magic:     await iconToBase64Png(FaMagic, `#${C.white}`),
    cogs:      await iconToBase64Png(FaCogs, `#${C.primary}`),
    file:      await iconToBase64Png(FaFileAlt, `#${C.primary}`),
    terminal:  await iconToBase64Png(FaTerminal, `#${C.white}`),
    bolt:      await iconToBase64Png(FaBolt, `#${C.accent}`),
    check:     await iconToBase64Png(FaCheckCircle, `#${C.accent}`),
    arrow:     await iconToBase64Png(FaArrowRight, `#${C.mid}`),
    // dark versions for light bg
    rocketDk:  await iconToBase64Png(FaRocket, `#${C.primary}`),
    searchW:   await iconToBase64Png(FaSearch, `#${C.white}`),
    penW:      await iconToBase64Png(FaPenFancy, `#${C.white}`),
    clipW:     await iconToBase64Png(FaClipboardList, `#${C.white}`),
    uploadW:   await iconToBase64Png(FaCloudUploadAlt, `#${C.white}`),
    checkW:    await iconToBase64Png(FaCheckCircle, `#${C.white}`),
  };

  // ============================================================
  // SLIDE 1: Title
  // ============================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.dark };

    // Decorative accent bar at top
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.accent }
    });

    // Rocket icon
    s.addImage({ data: icons.rocket, x: 4.5, y: 0.8, w: 1.0, h: 1.0 });

    // Title
    s.addText("generate-docs", {
      x: 0.5, y: 2.0, w: 9.0, h: 1.0,
      fontSize: 48, fontFace: "Trebuchet MS", bold: true,
      color: C.white, align: "center", margin: 0
    });

    // Subtitle
    s.addText("From codebase to published docs in one command", {
      x: 1.0, y: 3.0, w: 8.0, h: 0.6,
      fontSize: 20, fontFace: "Calibri",
      color: C.accent, align: "center", margin: 0
    });

    // Description
    s.addText("A Claude Code skill that reads your repo, plans documentation,\nand publishes it to ReadMe — automatically.", {
      x: 1.5, y: 3.8, w: 7.0, h: 0.8,
      fontSize: 14, fontFace: "Calibri",
      color: C.muted, align: "center", margin: 0
    });

    // Bottom bar
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 5.3, w: 10, h: 0.325, fill: { color: C.primary }
    });
    s.addText("ReadMe Hackathon 2025", {
      x: 0.5, y: 5.32, w: 9.0, h: 0.3,
      fontSize: 11, fontFace: "Calibri", color: C.white, align: "center", margin: 0
    });
  }

  // ============================================================
  // SLIDE 2: The Problem
  // ============================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.white };

    s.addText("The Problem", {
      x: 0.7, y: 0.4, w: 8.6, h: 0.7,
      fontSize: 36, fontFace: "Trebuchet MS", bold: true,
      color: C.dark, align: "left", margin: 0
    });

    // Left column — pain points as cards
    const pains = [
      { num: "1", title: "Writing docs is tedious", desc: "Engineers would rather ship features than write documentation pages from scratch." },
      { num: "2", title: "Docs fall out of date", desc: "Codebases evolve fast — documentation rarely keeps up with the actual implementation." },
      { num: "3", title: "No standard quality bar", desc: "Every project's docs look and feel different. There's no easy way to match Stripe-level quality." },
    ];

    pains.forEach((p, i) => {
      const yPos = 1.5 + i * 1.25;
      // Card background
      s.addShape(pres.shapes.RECTANGLE, {
        x: 0.7, y: yPos, w: 8.6, h: 1.05,
        fill: { color: C.card }, shadow: makeShadow()
      });
      // Number circle
      s.addShape(pres.shapes.OVAL, {
        x: 1.0, y: yPos + 0.2, w: 0.6, h: 0.6,
        fill: { color: C.primary }
      });
      s.addText(p.num, {
        x: 1.0, y: yPos + 0.2, w: 0.6, h: 0.6,
        fontSize: 18, fontFace: "Trebuchet MS", bold: true,
        color: C.white, align: "center", valign: "middle", margin: 0
      });
      // Title
      s.addText(p.title, {
        x: 1.85, y: yPos + 0.12, w: 7.0, h: 0.4,
        fontSize: 17, fontFace: "Trebuchet MS", bold: true,
        color: C.dark, margin: 0
      });
      // Description
      s.addText(p.desc, {
        x: 1.85, y: yPos + 0.52, w: 7.0, h: 0.4,
        fontSize: 13, fontFace: "Calibri",
        color: C.muted, margin: 0
      });
    });
  }

  // ============================================================
  // SLIDE 3: The Solution
  // ============================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.dark };

    s.addText("The Solution", {
      x: 0.7, y: 0.4, w: 8.6, h: 0.7,
      fontSize: 36, fontFace: "Trebuchet MS", bold: true,
      color: C.white, align: "left", margin: 0
    });

    s.addText("Point it at a repo. Pick a style. Get published docs.", {
      x: 0.7, y: 1.1, w: 8.6, h: 0.5,
      fontSize: 16, fontFace: "Calibri", italic: true,
      color: C.accent, margin: 0
    });

    // Three feature cards
    const features = [
      { icon: icons.magic, title: "AI-Powered", desc: "LLMs read your codebase, plan a table of contents, and write every guide." },
      { icon: icons.book,  title: "Style-Matched", desc: "Learns from Stripe, ReadMe, or Mintlify docs to match their quality." },
      { icon: icons.code,  title: "Fully Automated", desc: "Generates guides, llms.txt, OpenAPI spec, and uploads to ReadMe." },
    ];

    features.forEach((f, i) => {
      const xPos = 0.7 + i * 3.1;
      // Card
      s.addShape(pres.shapes.RECTANGLE, {
        x: xPos, y: 1.9, w: 2.8, h: 3.1,
        fill: { color: "0F2B36" }, shadow: makeShadow()
      });
      // Icon circle
      s.addShape(pres.shapes.OVAL, {
        x: xPos + 0.95, y: 2.2, w: 0.9, h: 0.9,
        fill: { color: C.primary }
      });
      s.addImage({ data: f.icon, x: xPos + 1.15, y: 2.4, w: 0.5, h: 0.5 });
      // Title
      s.addText(f.title, {
        x: xPos + 0.2, y: 3.3, w: 2.4, h: 0.5,
        fontSize: 18, fontFace: "Trebuchet MS", bold: true,
        color: C.white, align: "center", margin: 0
      });
      // Description
      s.addText(f.desc, {
        x: xPos + 0.2, y: 3.8, w: 2.4, h: 0.9,
        fontSize: 12, fontFace: "Calibri",
        color: C.muted, align: "center", margin: 0
      });
    });
  }

  // ============================================================
  // SLIDE 4: How It Works — The Pipeline
  // ============================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.white };

    s.addText("How It Works", {
      x: 0.7, y: 0.4, w: 8.6, h: 0.7,
      fontSize: 36, fontFace: "Trebuchet MS", bold: true,
      color: C.dark, align: "left", margin: 0
    });

    s.addText("Five-phase pipeline, each a standalone script", {
      x: 0.7, y: 1.05, w: 8.6, h: 0.4,
      fontSize: 14, fontFace: "Calibri",
      color: C.muted, margin: 0
    });

    const phases = [
      { icon: icons.search,    label: "Fetch\nExamples",  desc: "Download real docs\nfrom Stripe / ReadMe /\nMintlify as references" },
      { icon: icons.clipboard, label: "Plan\nGuides",     desc: "LLM scans codebase\nand proposes a table\nof contents" },
      { icon: icons.pen,       label: "Generate\nGuides",  desc: "LLM writes each guide\nwith frontmatter and\nllms.txt index" },
      { icon: icons.cogs,      label: "OpenAPI\nSpec",     desc: "Generate and upload\nOpenAPI 3.1 spec\nto ReadMe" },
      { icon: icons.upload,    label: "Upload\nGuides",    desc: "Push all guides to\nReadMe via rdme CLI" },
    ];

    phases.forEach((p, i) => {
      const xPos = 0.45 + i * 1.88;
      const yBase = 1.7;

      // Card
      s.addShape(pres.shapes.RECTANGLE, {
        x: xPos, y: yBase, w: 1.7, h: 3.4,
        fill: { color: C.card }, shadow: makeShadow()
      });

      // Phase number pill
      s.addShape(pres.shapes.RECTANGLE, {
        x: xPos + 0.55, y: yBase + 0.2, w: 0.6, h: 0.32,
        fill: { color: C.primary }
      });
      s.addText(`${i + 1}`, {
        x: xPos + 0.55, y: yBase + 0.2, w: 0.6, h: 0.32,
        fontSize: 13, fontFace: "Calibri", bold: true,
        color: C.white, align: "center", valign: "middle", margin: 0
      });

      // Icon
      s.addImage({ data: p.icon, x: xPos + 0.55, y: yBase + 0.75, w: 0.6, h: 0.6 });

      // Label
      s.addText(p.label, {
        x: xPos + 0.1, y: yBase + 1.5, w: 1.5, h: 0.7,
        fontSize: 13, fontFace: "Trebuchet MS", bold: true,
        color: C.dark, align: "center", valign: "top", margin: 0
      });

      // Description
      s.addText(p.desc, {
        x: xPos + 0.1, y: yBase + 2.2, w: 1.5, h: 1.0,
        fontSize: 10, fontFace: "Calibri",
        color: C.muted, align: "center", valign: "top", margin: 0
      });

      // Arrow between cards (not after last)
      if (i < phases.length - 1) {
        s.addImage({ data: icons.arrow, x: xPos + 1.78, y: yBase + 1.3, w: 0.3, h: 0.3 });
      }
    });
  }

  // ============================================================
  // SLIDE 5: Demo — What You Get
  // ============================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.white };

    s.addText("What You Get", {
      x: 0.7, y: 0.4, w: 8.6, h: 0.7,
      fontSize: 36, fontFace: "Trebuchet MS", bold: true,
      color: C.dark, align: "left", margin: 0
    });

    // Left column — output list
    const outputs = [
      { icon: icons.file,      title: "15 Documentation Guides", desc: "Overview, Getting Started, API Reference, Deployment, Troubleshooting, and more" },
      { icon: icons.rocketDk,  title: "llms.txt Index", desc: "LLM-optimized index linking all guides with descriptions" },
      { icon: icons.cogs,      title: "OpenAPI 3.1 Spec", desc: "Full API spec with 31 endpoints, schemas, and auth" },
      { icon: icons.check,     title: "Published to ReadMe", desc: "Guides and API reference live on your ReadMe project" },
    ];

    outputs.forEach((o, i) => {
      const yPos = 1.4 + i * 1.0;
      // Icon
      s.addImage({ data: o.icon, x: 0.9, y: yPos + 0.05, w: 0.45, h: 0.45 });
      // Title
      s.addText(o.title, {
        x: 1.6, y: yPos, w: 4.0, h: 0.35,
        fontSize: 15, fontFace: "Trebuchet MS", bold: true,
        color: C.dark, margin: 0
      });
      // Desc
      s.addText(o.desc, {
        x: 1.6, y: yPos + 0.35, w: 4.0, h: 0.35,
        fontSize: 11, fontFace: "Calibri",
        color: C.muted, margin: 0
      });
    });

    // Right side — code snippet card
    s.addShape(pres.shapes.RECTANGLE, {
      x: 5.9, y: 1.4, w: 3.7, h: 3.6,
      fill: { color: C.dark }, shadow: makeShadow()
    });

    s.addText("Just ask Claude Code:", {
      x: 6.1, y: 1.55, w: 3.3, h: 0.35,
      fontSize: 11, fontFace: "Calibri", italic: true,
      color: C.muted, margin: 0
    });

    const codeLines = [
      { text: '> generate docs for', options: { color: C.accent, fontSize: 13, fontFace: "Consolas", breakLine: true } },
      { text: '  /path/to/my/repo', options: { color: C.accent, fontSize: 13, fontFace: "Consolas", breakLine: true } },
      { text: '', options: { fontSize: 8, breakLine: true } },
      { text: 'Style: Stripe', options: { color: C.muted, fontSize: 11, fontFace: "Consolas", breakLine: true } },
      { text: 'Type:  Simple markdown', options: { color: C.muted, fontSize: 11, fontFace: "Consolas", breakLine: true } },
      { text: '', options: { fontSize: 8, breakLine: true } },
      { text: 'Planning 15 guides...', options: { color: "4DB8A4", fontSize: 11, fontFace: "Consolas", breakLine: true } },
      { text: 'Generating overview.md...', options: { color: "4DB8A4", fontSize: 11, fontFace: "Consolas", breakLine: true } },
      { text: 'Generating getting-started.md...', options: { color: "4DB8A4", fontSize: 11, fontFace: "Consolas", breakLine: true } },
      { text: '...', options: { color: C.muted, fontSize: 11, fontFace: "Consolas", breakLine: true } },
      { text: '', options: { fontSize: 8, breakLine: true } },
      { text: 'Uploaded 15 guides to ReadMe', options: { color: C.accent, fontSize: 11, fontFace: "Consolas", bold: true } },
    ];

    s.addText(codeLines, {
      x: 6.1, y: 2.0, w: 3.3, h: 2.8,
      valign: "top", margin: 0
    });
  }

  // ============================================================
  // SLIDE 6: Style Presets
  // ============================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.light };

    s.addText("Match Any Documentation Style", {
      x: 0.7, y: 0.4, w: 8.6, h: 0.7,
      fontSize: 36, fontFace: "Trebuchet MS", bold: true,
      color: C.dark, align: "left", margin: 0
    });

    s.addText("Fetch real docs via llms.txt to use as quality references for the LLM", {
      x: 0.7, y: 1.05, w: 8.6, h: 0.4,
      fontSize: 14, fontFace: "Calibri",
      color: C.muted, margin: 0
    });

    const presets = [
      { name: "Stripe", color: "635BFF", desc: "Clean, developer-first\npayment quickstarts\nand API auth guides", source: "docs.stripe.com" },
      { name: "ReadMe", color: "018EF5", desc: "Getting started guides,\nAPI reference setup,\nand interactive docs", source: "docs.readme.com" },
      { name: "Mintlify", color: "0D9373", desc: "Modern quickstarts,\nAPI playground setup,\nand navigation guides", source: "mintlify.com/docs" },
    ];

    presets.forEach((p, i) => {
      const xPos = 0.7 + i * 3.1;
      // Card
      s.addShape(pres.shapes.RECTANGLE, {
        x: xPos, y: 1.7, w: 2.8, h: 3.2,
        fill: { color: C.white }, shadow: makeShadow()
      });
      // Color bar at top
      s.addShape(pres.shapes.RECTANGLE, {
        x: xPos, y: 1.7, w: 2.8, h: 0.08,
        fill: { color: p.color }
      });
      // Name
      s.addText(p.name, {
        x: xPos + 0.3, y: 2.05, w: 2.2, h: 0.5,
        fontSize: 22, fontFace: "Trebuchet MS", bold: true,
        color: p.color, align: "left", margin: 0
      });
      // Source
      s.addText(p.source, {
        x: xPos + 0.3, y: 2.5, w: 2.2, h: 0.3,
        fontSize: 10, fontFace: "Consolas",
        color: C.muted, margin: 0
      });
      // Description
      s.addText(p.desc, {
        x: xPos + 0.3, y: 3.0, w: 2.2, h: 1.2,
        fontSize: 12, fontFace: "Calibri",
        color: C.text, margin: 0
      });
      // Or custom
      if (i === 2) {
        s.addText("+ any custom URL", {
          x: xPos + 0.3, y: 4.2, w: 2.2, h: 0.4,
          fontSize: 11, fontFace: "Calibri", italic: true,
          color: C.primary, margin: 0
        });
      }
    });
  }

  // ============================================================
  // SLIDE 7: Architecture
  // ============================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.white };

    s.addText("Architecture", {
      x: 0.7, y: 0.4, w: 8.6, h: 0.7,
      fontSize: 36, fontFace: "Trebuchet MS", bold: true,
      color: C.dark, align: "left", margin: 0
    });

    s.addText("Each phase is a standalone Python script — composable and debuggable", {
      x: 0.7, y: 1.05, w: 8.6, h: 0.4,
      fontSize: 14, fontFace: "Calibri",
      color: C.muted, margin: 0
    });

    // File tree card
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.7, y: 1.6, w: 4.2, h: 3.6,
      fill: { color: C.dark }, shadow: makeShadow()
    });

    const treeLines = [
      { text: "scripts/", options: { color: C.accent, fontSize: 12, fontFace: "Consolas", bold: true, breakLine: true } },
      { text: "  fetch_examples.py", options: { color: "7DD3C8", fontSize: 12, fontFace: "Consolas", breakLine: true } },
      { text: "  plan_guides.py", options: { color: "7DD3C8", fontSize: 12, fontFace: "Consolas", breakLine: true } },
      { text: "  generate_guides.py", options: { color: "7DD3C8", fontSize: 12, fontFace: "Consolas", breakLine: true } },
      { text: "  upload_openapi.py", options: { color: "7DD3C8", fontSize: 12, fontFace: "Consolas", breakLine: true } },
      { text: "  upload_guides.py", options: { color: "7DD3C8", fontSize: 12, fontFace: "Consolas", breakLine: true } },
      { text: "  run.py", options: { color: C.accent, fontSize: 12, fontFace: "Consolas", breakLine: true } },
      { text: "", options: { fontSize: 6, breakLine: true } },
      { text: "references/", options: { color: C.accent, fontSize: 12, fontFace: "Consolas", bold: true, breakLine: true } },
      { text: "  stripe_llms.txt", options: { color: "7DD3C8", fontSize: 12, fontFace: "Consolas", breakLine: true } },
      { text: "  readme_llms.txt", options: { color: "7DD3C8", fontSize: 12, fontFace: "Consolas", breakLine: true } },
      { text: "  mintlify_llms.txt", options: { color: "7DD3C8", fontSize: 12, fontFace: "Consolas" } },
    ];

    s.addText(treeLines, {
      x: 1.0, y: 1.8, w: 3.6, h: 3.2,
      valign: "top", margin: 0
    });

    // Right side — tech stack
    const stack = [
      { label: "LLM Engine", value: "Claude Sonnet 4.5 via OpenRouter" },
      { label: "Codebase Scan", value: "Recursive .md glob (120K char budget)" },
      { label: "Style Learning", value: "Fetches .md from llms.txt URLs" },
      { label: "Output Format", value: "Markdown + YAML frontmatter" },
      { label: "Upload CLI", value: "rdme (ReadMe's official CLI)" },
      { label: "Orchestration", value: "Claude Code skill or standalone CLI" },
    ];

    stack.forEach((item, i) => {
      const yPos = 1.7 + i * 0.58;
      s.addShape(pres.shapes.RECTANGLE, {
        x: 5.3, y: yPos, w: 4.3, h: 0.48,
        fill: { color: i % 2 === 0 ? C.card : C.white }
      });
      s.addText(item.label, {
        x: 5.5, y: yPos, w: 1.7, h: 0.48,
        fontSize: 11, fontFace: "Trebuchet MS", bold: true,
        color: C.primary, valign: "middle", margin: 0
      });
      s.addText(item.value, {
        x: 7.2, y: yPos, w: 2.3, h: 0.48,
        fontSize: 11, fontFace: "Calibri",
        color: C.text, valign: "middle", margin: 0
      });
    });
  }

  // ============================================================
  // SLIDE 8: Live Results
  // ============================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.dark };

    s.addText("Real Results", {
      x: 0.7, y: 0.4, w: 8.6, h: 0.7,
      fontSize: 36, fontFace: "Trebuchet MS", bold: true,
      color: C.white, align: "left", margin: 0
    });

    s.addText("We ran it on ReadMe's AI service codebase", {
      x: 0.7, y: 1.05, w: 8.6, h: 0.4,
      fontSize: 14, fontFace: "Calibri", italic: true,
      color: C.accent, margin: 0
    });

    // Stats row
    const stats = [
      { num: "15", label: "Guides\nGenerated" },
      { num: "31", label: "API Endpoints\nDocumented" },
      { num: "9", label: "Style Examples\nFetched" },
      { num: "~5", label: "Minutes\nEnd to End" },
    ];

    stats.forEach((st, i) => {
      const xPos = 0.7 + i * 2.35;
      s.addShape(pres.shapes.RECTANGLE, {
        x: xPos, y: 1.7, w: 2.1, h: 1.6,
        fill: { color: "0F2B36" }, shadow: makeShadow()
      });
      s.addText(st.num, {
        x: xPos, y: 1.85, w: 2.1, h: 0.7,
        fontSize: 40, fontFace: "Trebuchet MS", bold: true,
        color: C.accent, align: "center", margin: 0
      });
      s.addText(st.label, {
        x: xPos, y: 2.55, w: 2.1, h: 0.6,
        fontSize: 12, fontFace: "Calibri",
        color: C.muted, align: "center", margin: 0
      });
    });

    // Sample guides list
    s.addText("Generated Guides", {
      x: 0.7, y: 3.6, w: 4.0, h: 0.4,
      fontSize: 14, fontFace: "Trebuchet MS", bold: true,
      color: C.white, margin: 0
    });

    const guideNames = [
      "overview.md", "getting-started.md", "mcp-server.md",
      "ask-ai-chat.md", "ai-agent.md", "vectorization.md",
      "api-reference.md", "deployment.md"
    ];

    s.addText(
      guideNames.map((g, i) => ({
        text: g,
        options: {
          fontSize: 11, fontFace: "Consolas", color: "7DD3C8",
          bullet: true,
          breakLine: i < guideNames.length - 1
        }
      })),
      { x: 0.7, y: 3.95, w: 4.0, h: 1.5, margin: 0 }
    );

    // Right side: llms.txt preview
    s.addText("llms.txt Output", {
      x: 5.3, y: 3.6, w: 4.3, h: 0.4,
      fontSize: 14, fontFace: "Trebuchet MS", bold: true,
      color: C.white, margin: 0
    });

    s.addShape(pres.shapes.RECTANGLE, {
      x: 5.3, y: 3.95, w: 4.3, h: 1.5,
      fill: { color: "0F2B36" }
    });

    const llmsPreview = [
      { text: "# ReadMe AI Documentation", options: { color: C.accent, fontSize: 10, fontFace: "Consolas", bold: true, breakLine: true } },
      { text: "## Docs", options: { color: C.accent, fontSize: 10, fontFace: "Consolas", breakLine: true } },
      { text: "- [Overview](guides/overview.md):", options: { color: "7DD3C8", fontSize: 9, fontFace: "Consolas", breakLine: true } },
      { text: "  Introduction to the AI Service", options: { color: C.muted, fontSize: 9, fontFace: "Consolas", breakLine: true } },
      { text: "- [Getting Started](...): Setup", options: { color: "7DD3C8", fontSize: 9, fontFace: "Consolas", breakLine: true } },
      { text: "- [MCP Server](...): MCP guide", options: { color: "7DD3C8", fontSize: 9, fontFace: "Consolas", breakLine: true } },
      { text: "  ...", options: { color: C.muted, fontSize: 9, fontFace: "Consolas" } },
    ];

    s.addText(llmsPreview, {
      x: 5.5, y: 4.05, w: 3.9, h: 1.3,
      valign: "top", margin: 0
    });
  }

  // ============================================================
  // SLIDE 9: Closing / CTA
  // ============================================================
  {
    const s = pres.addSlide();
    s.background = { color: C.dark };

    // Top accent bar
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.accent }
    });

    s.addImage({ data: icons.rocket, x: 4.5, y: 0.7, w: 1.0, h: 1.0 });

    s.addText("generate-docs", {
      x: 0.5, y: 1.9, w: 9.0, h: 0.8,
      fontSize: 44, fontFace: "Trebuchet MS", bold: true,
      color: C.white, align: "center", margin: 0
    });

    s.addText("Every repo deserves great docs.\nNow they can have them in minutes.", {
      x: 1.5, y: 2.8, w: 7.0, h: 0.8,
      fontSize: 18, fontFace: "Calibri",
      color: C.accent, align: "center", margin: 0
    });

    // Three takeaway pills
    const takeaways = ["AI-Generated", "Style-Matched", "Auto-Published"];
    takeaways.forEach((t, i) => {
      const xPos = 1.7 + i * 2.4;
      s.addShape(pres.shapes.RECTANGLE, {
        x: xPos, y: 3.9, w: 2.0, h: 0.45,
        fill: { color: C.primary }
      });
      s.addText(t, {
        x: xPos, y: 3.9, w: 2.0, h: 0.45,
        fontSize: 13, fontFace: "Calibri", bold: true,
        color: C.white, align: "center", valign: "middle", margin: 0
      });
    });

    // Bottom bar
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 5.3, w: 10, h: 0.325, fill: { color: C.primary }
    });
    s.addText("Thank you!", {
      x: 0.5, y: 5.32, w: 9.0, h: 0.3,
      fontSize: 13, fontFace: "Calibri", bold: true,
      color: C.white, align: "center", margin: 0
    });
  }

  // Write file
  const outPath = "/Users/xineohperif/projects/lyra/readme/hackathon/generate-docs-pitch.pptx";
  await pres.writeFile({ fileName: outPath });
  console.log(`Presentation saved to ${outPath}`);
}

main().catch(err => { console.error(err); process.exit(1); });
