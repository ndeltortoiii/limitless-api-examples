import dotenv from "dotenv";
import { getLifelogs } from "./_client";
import { TodoistApi, Task } from "@doist/todoist-api-typescript";

// Load environment variables
dotenv.config();

const TODOIST_API_TOKEN = process.env.TODOIST_API_TOKEN;
const TODOIST_TASK_ID = "6X9H6gpXmPxpHGXc";

// Initialize Todoist API client
const todoistApi = new TodoistApi(TODOIST_API_TOKEN || "");

// Function to get all sub-tasks of a specific task
async function getSubTasks(taskId: string): Promise<Task[]> {
  console.log(`\n📋 Fetching existing sub-tasks for task ID: ${taskId}...`);
  try {
    const response = await fetch(
      `https://api.todoist.com/rest/v2/tasks?parent_id=${taskId}`,
      {
        headers: {
          Authorization: `Bearer ${TODOIST_API_TOKEN}`,
        },
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const tasks = await response.json();
    // Filter for tasks that are not completed
    const subTasks = tasks.filter((task: Task) => !task.isCompleted);
    console.log(
      `✅ Found ${subTasks.length} existing sub-tasks for task ${taskId}`
    );
    return subTasks;
  } catch (error) {
    console.error("❌ Error fetching sub-tasks:", error);
    return [];
  }
}

// Function to add a new sub-task
async function addSubTask(content: string): Promise<void> {
  console.log(`\n➕ Attempting to add new sub-task: "${content}"`);
  try {
    await todoistApi.addTask({
      content,
      parentId: TODOIST_TASK_ID,
    });
    console.log(`✅ Successfully added sub-task: "${content}"`);
  } catch (error) {
    console.error(`❌ Failed to add sub-task "${content}":`, error);
  }
}

// Function to extract task from a sentence
function extractTask(sentence: string): string | null {
  // Match "add" followed by any words until "to my to-do list"
  const match = sentence.match(/add\s+(.+?)\s+to\s+my\s+to-do\s+list/i);
  if (match && match[1]) {
    const words = match[1].trim().split(/\s+/);
    // Capitalize only the first word, lowercase the rest
    return words
      .map((word, index) =>
        index === 0
          ? word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
          : word.toLowerCase()
      )
      .join(" ");
  }
  return null;
}

// Keep track of processed lines for each entry
const processedLines = new Map<string, Set<string>>();

// Function to process lifelog entries and extract to-do items
async function processLifelogs(lifelogs: any[]): Promise<void> {
  console.log(`\n📝 Processing ${lifelogs.length} lifelog entries...`);

  // Get existing sub-tasks
  const existingSubTasks = await getSubTasks(TODOIST_TASK_ID);

  // Create a map of lowercase content to task for easy lookup
  const existingTasksMap = new Map(
    existingSubTasks.map((task) => [task.content.toLowerCase().trim(), task])
  );

  let foundMatches = 0;
  let addedTasks = 0;
  let skippedTasks = 0;
  let emptyTasks = 0;

  console.log("\n📜 Reviewing lifelog entries:");
  console.log("=".repeat(80));

  for (const [index, lifelog] of lifelogs.entries()) {
    const content = lifelog.markdown || "";
    const hasMatch =
      content.toLowerCase().includes("add") &&
      content.toLowerCase().includes("to my to-do list");

    if (hasMatch) {
      console.log(`\n📄 Entry ${index + 1}/${lifelogs.length}:`);
      console.log("-".repeat(40));
      foundMatches++;
      console.log(`🔍 Found potential task addition in lifelog entry`);

      // Extract sentences
      const sentences = content.split(/[.!?]+/);
      for (const sentence of sentences) {
        // Skip if we've already processed this exact line
        if (processedLines.get(lifelog.id)?.has(sentence.trim())) {
          continue;
        }

        const taskContent = extractTask(sentence);

        if (taskContent) {
          const normalizedTaskContent = taskContent.toLowerCase().trim();
          console.log(`\n📝 Processing sentence: "${sentence}"`);
          console.log(`📌 Extracted task: "${taskContent}"`);
          console.log(`🔍 Normalized task content: "${normalizedTaskContent}"`);

          const existingTask = existingTasksMap.get(normalizedTaskContent);
          if (existingTask) {
            console.log(`ℹ️ Found existing task:`);
            console.log(`   Raw content: "${existingTask.content}"`);
            console.log(
              `   Normalized: "${existingTask.content.toLowerCase().trim()}"`
            );
            console.log(`   Completed: ${existingTask.isCompleted}`);
            console.log(`   ID: ${existingTask.id}`);

            if (existingTask.isCompleted) {
              console.log(
                `✨ Found completed task, adding as new task: "${taskContent}"`
              );
              await addSubTask(taskContent);
              addedTasks++;
            } else {
              console.log(
                `ℹ️ Task already exists and is not completed, skipping: "${taskContent}"`
              );
              skippedTasks++;
            }
          } else {
            console.log(`✨ This is a new task, adding to Todoist...`);
            await addSubTask(taskContent);
            addedTasks++;
            // Add to our map to prevent duplicates within the same run
            existingTasksMap.set(normalizedTaskContent, {
              content: taskContent,
              isCompleted: false,
            } as Task);
          }

          // Mark this line as processed
          if (!processedLines.has(lifelog.id)) {
            processedLines.set(lifelog.id, new Set());
          }
          processedLines.get(lifelog.id)!.add(sentence.trim());
        }
      }
      console.log("-".repeat(40));
    }
  }

  console.log(`\n📊 Summary:`);
  console.log(`- Processed ${lifelogs.length} lifelog entries`);
  console.log(`- Found ${foundMatches} entries containing task additions`);
  console.log(`- Added ${addedTasks} new tasks to Todoist`);
  console.log(`- Skipped ${skippedTasks} duplicate tasks (not completed)`);
  console.log(`- Found ${emptyTasks} unparseable task additions`);
}

// Main function
async function main(): Promise<void> {
  console.log("🚀 Starting to-do list monitor...");

  if (!TODOIST_API_TOKEN) {
    console.error(
      "❌ Error: TODOIST_API_TOKEN environment variable is not set"
    );
    process.exit(1);
  }

  try {
    while (true) {
      console.log("\n📥 Checking for new lifelog entries...");
      // Get the most recent lifelogs
      const lifelogs = await getLifelogs({
        apiKey: process.env.LIMITLESS_API_KEY || "",
        limit: 10, // Adjust this number based on how many recent entries you want to check
        direction: "desc",
      });

      if (lifelogs.length > 0) {
        // Process all entries every time, our processLifelogs function will handle duplicates
        await processLifelogs(lifelogs);
      }

      // Wait 3 seconds before checking again
      await new Promise((resolve) => setTimeout(resolve, 3000));
    }
  } catch (error) {
    console.error("❌ Error:", error);
    process.exit(1);
  }
}

// Run the main function
main();
