import axios from "axios"

const scraperUrl = "http://localhost:9080/scrape"

export const scrape = async (params) => {
  var bodyFormData = new FormData();
  Object.keys(params).forEach(key =>
    bodyFormData.append(key, params[key])
  )
  try {
    const response = await axios({
      method: 'post',
      url: scraperUrl,
      data: bodyFormData,
      headers: { "Content-Type": "multipart/form-data" },
    })
    return response.data
  }
  catch (e) {
    console.error(e)
    throw Error(e.response.data.error.message)
  }

}