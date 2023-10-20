import React, { useContext, useState } from "react";
import "./SearchBox.css"
import {ReactComponent as SearchIcon} from "../assets/icons/Frame.svg"
import {ReactComponent as ResibarIcon} from "../assets/icons/icon-park-solid_voice.svg"
import {ReactComponent as ArrowIcon} from "../assets/icons/ic_baseline-arrow-forward.svg"
import { ProductContext } from "../commons/Home";

const SearchBox = () => {
    const [query, setQuery] = useState("")
    const {message, setMessage} = useContext(ProductContext)
    const data = {query}

    const handleSendMessage =async () => {
        if (!query.trim() == ""){
            setMessage(message => [
                ...message,
                {user: "USER", text: query},
                {user: "BOT", text: "LOADING"}
            ])
            
            try {
                const res = await fetch('/api/chat', {
                    method: "POST",
                    body: JSON.stringify(data)
                })
                if (res.ok) {
                    setQuery("")
                    console.log('....................')

                    const response = await res.json()
                    console.log('response:  ', response)

                    // setMessage(response.message)
                    setMessage(message => [
                        ...message.filter((item) => item.text !== "LOADING"),
                        {user: "BOT", text: response.message}
                    ])
                }
            } catch (err) {

            }
            setMessage(message => message.filter((item) => item.text !== "LOADING"))
            
        }
    }

    return (
        <div className="searchbox-wrapper">
            <div className="search-icon">
                <span><SearchIcon /></span>
            </div>
            <div className="search-input">
                <input value={query} placeholder="Search your Products" onChange={(e) => setQuery(e.target.value)}/>
            </div>
            <div className="resibar-icon">
                <span><ResibarIcon /></span>
            </div>
            <div className="arrow-icon" onClick={handleSendMessage}>
                <span><ArrowIcon /></span>
            </div>
        </div>
    )
}

export default SearchBox;