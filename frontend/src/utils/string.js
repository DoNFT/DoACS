export function stringCompare(str1 = '', str2 = '') {
    if(!str1) str1 = ''
    if(!str2) str2 = ''
    return !str1.localeCompare(str2, undefined, {sensitivity:'accent'})
}

export function catToFixed(str = ''){
    if((typeof str).toLowerCase() !== 'string') return ''
    const maxLength = 10
    if(str.length <= maxLength) return str;
    return `${str.slice(0, 6)}...${str.slice(-4)}`
}

export function shortCat(str = '', maxLength = 30){
    if((typeof str).toLowerCase() !== 'string') return ''
    if(str.length <= maxLength) return str;
    return `${str.slice(0, maxLength)}...`
}