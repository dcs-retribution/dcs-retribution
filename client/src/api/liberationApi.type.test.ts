import { Tgo } from "./_liberationApi";

// The backend serializes Optional[tuple[str, str]] as a two-string tuple.
const task: Tgo["task"] = ["LORAD", "Anti Air"];

// Keep this fixture honest: a variable-length array must not satisfy Tgo.task.
const variableLengthTask: string[] = ["LORAD", "Anti Air", "unexpected"];
// @ts-expect-error Tgo.task is exactly a two-string tuple, not string[].
const invalidTask: Tgo["task"] = variableLengthTask;

test("Tgo task accepts the backend tuple shape", () => {
  expect(task).toEqual(["LORAD", "Anti Air"]);
});

void invalidTask;
