import axios from "axios";

const jobsUrl = "http://localhost:9080/jobs"

export const eventSource = new EventSource(jobsUrl + "?stream=true");

export const removeJob = async (id) => {
  try {
    const response = await axios.delete(
      jobsUrl + `/${id}`
    )
    console.log(response)
    return response.data
  }
  catch (e) {
    console.error(e)
    throw Error(e.response.data.error.message)
  }

}