import { getSession, updateSession, clearSession } from "./memory";
import fs from "node:fs";


const [cmd, userId, json] = process.argv.slice(2);
if (cmd === "get") console.log(JSON.stringify(getSession(userId)));
else if (cmd === "update") { updateSession(userId, JSON.parse(fs.readFileSync(json, "utf8"))); console.log("session updated"); }
else if (cmd === "clear") { clearSession(userId); console.log("session cleared"); }