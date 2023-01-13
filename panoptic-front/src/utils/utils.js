import { DASHBOARD_URL } from "./const"

export const openElastic = (imageList) => {
    const url = forge_url(imageList.map(e => e.name))
    window.open(url, '_blank').focus();
}

export const forge_url = (imageList) => {
    const encodedImageList = imageList.map(image => {
        const sha1 = image.split('/').slice(-1)[0].split('.')[0]
        return "media_sha1s.keyword:%20%22" + sha1 + "%22" 
    })
    const query = "'" + encodedImageList.join('%20or%20') + "'),filters:!())"
    return DASHBOARD_URL + query
}