import axios from "axios"

const spidersUrl = 'http://localhost:9080/spiders'
export const getSpiders = async () => {
  const response = await axios.get(spidersUrl)
  if (response.status === 200) {
    return response.data.spiders
  } else {
    return []
  }

}