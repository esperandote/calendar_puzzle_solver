import { message } from 'ant-design-vue'

const buildQueryParams = (data) => {
    return Object.keys(data)
        .map((key, index) => `${index === 0 ? '?' : '&'}${key}=${encodeURIComponent(data[key])}`)
        .join('')
}

export const getRequest = async (url, data) => {
    const requestOptions = {
        method: "GET",
    }
    const response = await fetch(window.location.origin + url + buildQueryParams(data), requestOptions)

    const responseData = await response.json().catch(() => {
        message.error('无法连接服务器')
        return { status: 400, error: '无法连接服务器' }
    })
    return {
        status: response.status,
        ...responseData,
    }
}

export const postRequest = async (url, data) => {
    const headers = new Headers()
    headers.append('Content-Type', 'application/json');
    const requestOptions = {
        method: "POST",
        headers: headers,
        body: JSON.stringify(data)
    }
    const response = await fetch(window.location.origin + url, requestOptions)

    const responseData = await response.json().catch(() => {
        message.error('无法连接服务器')
        return { status: 400, error: '无法连接服务器' }
    })
    return {
        status: response.status,
        ...responseData,
    }
}