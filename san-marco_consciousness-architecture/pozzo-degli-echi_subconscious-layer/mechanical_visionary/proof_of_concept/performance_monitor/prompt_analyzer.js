#!/usr/bin/env node

/**
 * Prompt Analyzer for Thinking Mode Optimization
 * Analyzes prompt complexity and suggests optimal thinking depth
 */

const fs = require('fs');
const path = require('path');

// Parse command line arguments
const userPrompt = process.argv[2] || '';

// Analyze prompt complexity
function analyzeComplexity(prompt) {
  const factors = {
    length: prompt.length,
    questions: (prompt.match(/\?/g) || []).length,
    keywords: {
      analysis: /analyz|investigat|examin|evaluat/i.test(prompt),
      creation: /creat|build|design|implement|develop/i.test(prompt),
      strategy: /strateg|plan|architect|roadmap/i.test(prompt),
      debug: /debug|fix|troubleshoot|error|issue/i.test(prompt),
      multiple: /multiple|several|various|list|all/i.test(prompt),
      critical: /critical|urgent|important|essential|crucial/i.test(prompt),
      complex: /complex|complicated|intricate|sophisticated/i.test(prompt)
    },
    codeBlocks: (prompt.match(/```/g) || []).length / 2,
    listItems: (prompt.match(/^[\s]*[-*\d]/gm) || []).length
  };
  
  // Calculate complexity score
  let score = 0;
  
  // Length factor
  if (factors.length > 500) score += 2;
  if (factors.length > 1000) score += 3;
  
  // Question complexity
  score += factors.questions * 1.5;
  
  // Keyword analysis
  Object.values(factors.keywords).forEach(matches => {
    if (matches) score += 2;
  });
  
  // Code analysis tasks are complex
  score += factors.codeBlocks * 3;
  
  // Multiple items increase complexity
  score += factors.listItems * 0.5;
  
  return { score, factors };
}

// Determine optimal thinking mode
function getThinkingMode(score) {
  if (score < 3) return { mode: 'standard', trigger: 'think', tokens: 4000 };
  if (score < 7) return { mode: 'enhanced', trigger: 'think hard', tokens: 10000 };
  if (score < 12) return { mode: 'deep', trigger: 'megathink', tokens: 10000 };
  return { mode: 'maximum', trigger: 'ultrathink', tokens: 31999 };
}

// Analyze the prompt
const analysis = analyzeComplexity(userPrompt);
const thinkingMode = getThinkingMode(analysis.score);

// Generate optimization suggestions
const suggestions = [];

if (analysis.factors.keywords.multiple) {
  suggestions.push('Consider breaking this into sequential tasks for better results');
}

if (analysis.factors.codeBlocks > 2) {
  suggestions.push('Complex code analysis detected - extended thinking recommended');
}

if (analysis.factors.keywords.critical && analysis.score < 10) {
  suggestions.push('Critical task detected but low complexity - verify requirements');
}

// Log analysis results
const analysisPath = path.join(__dirname, 'prompt_analysis.json');
let allAnalyses = [];

try {
  if (fs.existsSync(analysisPath)) {
    allAnalyses = JSON.parse(fs.readFileSync(analysisPath, 'utf8'));
  }
} catch (e) {
  // Start fresh
}

const analysisResult = {
  timestamp: new Date().toISOString(),
  promptLength: userPrompt.length,
  complexity: analysis,
  recommendedMode: thinkingMode,
  suggestions: suggestions
};

allAnalyses.push(analysisResult);

// Keep only last 100 analyses
if (allAnalyses.length > 100) {
  allAnalyses = allAnalyses.slice(-100);
}

fs.writeFileSync(analysisPath, JSON.stringify(allAnalyses, null, 2));

// Calculate insights from recent analyses
const recentAnalyses = allAnalyses.slice(-20);
const avgComplexity = recentAnalyses.reduce((sum, a) => sum + a.complexity.score, 0) / recentAnalyses.length;
const modeDistribution = recentAnalyses.reduce((dist, a) => {
  dist[a.recommendedMode.mode] = (dist[a.recommendedMode.mode] || 0) + 1;
  return dist;
}, {});

// Save insights
const insightsPath = path.join(__dirname, 'thinking_insights.json');
const insights = {
  timestamp: new Date().toISOString(),
  averageComplexity: avgComplexity.toFixed(2),
  modeDistribution: modeDistribution,
  recommendations: []
};

if (avgComplexity > 10) {
  insights.recommendations.push('High average complexity - consider task decomposition strategies');
}

if (modeDistribution.maximum > recentAnalyses.length * 0.3) {
  insights.recommendations.push('Frequent maximum thinking usage - optimize prompts for efficiency');
}

fs.writeFileSync(insightsPath, JSON.stringify(insights, null, 2));

// Return optimization hints to Claude
const response = {
  thinkingOptimization: {
    suggestedMode: thinkingMode.mode,
    suggestedTrigger: thinkingMode.trigger,
    estimatedTokens: thinkingMode.tokens,
    complexityScore: analysis.score,
    optimizationHints: suggestions
  }
};

console.log(JSON.stringify(response));