#!/usr/bin/env node

/**
 * Test script for Cyber Fortune Telling MCP Server
 * This script can be used to test the MCP server functionality locally
 */

import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

console.log('🧪 Testing Cyber Fortune Telling MCP Server...\n');

// Test configuration
const TEST_CONFIG = {
  API_BASE_URL: process.env.CYBER_FORTUNE_API_BASE_URL || 'http://localhost:11337/api',
  TEST_USER_ID: 'zhaoolee',
  TEST_DATE: '2025-07-13'
};

console.log('Test Configuration:');
console.log(`API Base URL: ${TEST_CONFIG.API_BASE_URL}`);
console.log(`Test User ID: ${TEST_CONFIG.TEST_USER_ID}`);
console.log(`Test Date: ${TEST_CONFIG.TEST_DATE}\n`);

// Function to send MCP request and parse response
function sendMCPRequest(request) {
  return new Promise((resolve, reject) => {
    const serverPath = join(__dirname, 'index.js');
    const child = spawn('node', [serverPath], {
      stdio: ['pipe', 'pipe', 'pipe'],
      env: { ...process.env, CYBER_FORTUNE_API_BASE_URL: TEST_CONFIG.API_BASE_URL }
    });

    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    child.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    child.on('close', (code) => {
      if (code === 0) {
        try {
          const lines = stdout.trim().split('\n').filter(line => line.trim());
          const responses = lines.map(line => {
            try {
              return JSON.parse(line);
            } catch {
              return null;
            }
          }).filter(Boolean);
          resolve(responses);
        } catch (error) {
          reject(new Error(`Failed to parse response: ${error.message}`));
        }
      } else {
        reject(new Error(`Server exited with code ${code}. stderr: ${stderr}`));
      }
    });

    child.on('error', (error) => {
      reject(error);
    });

    // Send the request
    child.stdin.write(JSON.stringify(request) + '\n');
    child.stdin.end();
  });
}

// Test cases
const tests = [
  {
    name: 'List Tools',
    request: {
      jsonrpc: '2.0',
      id: 1,
      method: 'tools/list'
    }
  },
  {
    name: 'Get Conversation History',
    request: {
      jsonrpc: '2.0',
      id: 2,
      method: 'tools/call',
      params: {
        name: 'get_conversation_history',
        arguments: {
          fortune_telling_uid: TEST_CONFIG.TEST_USER_ID,
          date: TEST_CONFIG.TEST_DATE
        }
      }
    }
  },
  {
    name: 'Get Desk Decoration Info',
    request: {
      jsonrpc: '2.0',
      id: 3,
      method: 'tools/call',
      params: {
        name: 'get_desk_decoration_info',
        arguments: {
          fortune_telling_uid: TEST_CONFIG.TEST_USER_ID,
          date: TEST_CONFIG.TEST_DATE
        }
      }
    }
  }
];

// Run tests
async function runTests() {
  console.log('🚀 Starting MCP Server Tests...\n');

  for (const test of tests) {
    try {
      console.log(`⏳ Running test: ${test.name}`);
      const startTime = Date.now();
      
      const responses = await sendMCPRequest(test.request);
      const endTime = Date.now();
      
      if (responses.length > 0) {
        console.log(`✅ ${test.name} - Success (${endTime - startTime}ms)`);
        console.log(`Response:`, JSON.stringify(responses[0], null, 2));
      } else {
        console.log(`❌ ${test.name} - No response received`);
      }
    } catch (error) {
      console.log(`❌ ${test.name} - Error: ${error.message}`);
    }
    console.log(''); // Empty line between tests
  }

  console.log('🏁 Tests completed!\n');
  console.log('💡 To use with MCP Inspector:');
  console.log('1. Install MCP Inspector: npm install -g @modelcontextprotocol/inspector');
  console.log('2. Run: npx @modelcontextprotocol/inspector mcp.json');
  console.log('3. Test the tools in the web interface');
}

// Run the tests
runTests().catch((error) => {
  console.error('Fatal error in tests:', error);
  process.exit(1);
}); 