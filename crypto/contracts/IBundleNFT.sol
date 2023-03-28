//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";


interface IBundleNFT {
    enum TokenRole {
        NoRole,
        Original,
        Modifier
    }

    struct NFT {
        IERC721 token;
        uint256 tokenId;
        TokenRole role;
    }

    function bundle(NFT[] memory _tokens) external payable returns (uint256);
    function addNFTsToBundle(uint256 tokenId, NFT[] memory _tokens, string memory tokenURI) external payable;
    function removeNFTsFromBundle(uint256 _tokenId, NFT[] memory _tokens, string memory tokenURI) external payable;
    function unbundle(uint256 _tokenId) external payable;
}
