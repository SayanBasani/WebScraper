import { backend_Url } from "@/config";
import axios from "axios";

export async function getSummery(URL: string) {
  try {
    const res: any = await axios.post(
      backend_Url + "/scrape/",
      { q: URL },
      { withCredentials: true,headers: { "Content-Type": "application/json" } }
    );
    console.log(res);
    console.log(res.data);
    return res.data;
  } catch (error: any) {
    return { error: true, msg: error.response?.data || error.message };
  }
}
