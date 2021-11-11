import axios from 'axios'
import Cookies from "js-cookie";

export default axios.create({
  headers: {
    "content-type": "application/json",
    "X-CSRFToken": Cookies.get("csrftoken")
  }
})
