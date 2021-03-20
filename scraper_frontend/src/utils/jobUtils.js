export const JobStates = {
  FINISHED: "finished",
  CANCELLED: "cancelled",
  RUNNING: "running",
  SCHEDULED: "scheduled",
}

export const ActiveJobStates = [JobStates.SCHEDULED, JobStates.RUNNING]

export const InactiveJobStates = Object.values(JobStates).filter(e => !ActiveJobStates.includes(e))