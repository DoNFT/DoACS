//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";


/**
 * This contract maintains a list of modifiers collections,
 * approved by voting.
 */
contract EffectsAllowList is AccessControl {
    enum CollectionType {
        Colour,
        Item,
        Character,
        Achievement,
        None
    }

    struct EffectInfo {
        address modificatorsContract;
        string serverUrl;
        address owner;
        address originalContract;
        CollectionType collectionType;
    }

    bytes32 public constant LIST_MANAGER_ROLE = keccak256("LIST_MANAGER_ROLE");
    EffectInfo[] public effectsInfos;
    mapping(address => uint256) private effectToPositionInList;

    constructor() {
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _setupRole(LIST_MANAGER_ROLE, msg.sender);
    }


    function addToList(EffectInfo calldata effectInfo) public {
        require(hasRole(LIST_MANAGER_ROLE, msg.sender));
        require(effectInfo.modificatorsContract != address(0x0));

        effectToPositionInList[effectInfo.modificatorsContract] = effectsInfos.length;
        effectsInfos.push(effectInfo);
    }

    function removeFromList(address modificatorsContract) public {
        require(hasRole(LIST_MANAGER_ROLE, msg.sender));
        require(getByEffect(modificatorsContract).modificatorsContract == modificatorsContract);

        uint256 lastEffectIndex = effectsInfos.length - 1;
        uint256 removedEffectIndex = effectToPositionInList[modificatorsContract];

        // When the token to delete is the last token, the swap operation is unnecessary
        if (removedEffectIndex != lastEffectIndex) {
            effectsInfos[removedEffectIndex] = effectsInfos[lastEffectIndex];
            effectToPositionInList[effectsInfos[lastEffectIndex].modificatorsContract] = removedEffectIndex;
        }

        // This also deletes the contents at the last position of the array
        effectsInfos.pop();
        delete effectToPositionInList[modificatorsContract];
    }

    function checkPermission(address originalContract, address modificatorsContract) view public returns(bool) {
        if (effectsInfos.length == 0) return false;
        EffectInfo memory ei = getByEffect(modificatorsContract);
        return ei.modificatorsContract == modificatorsContract && (ei.originalContract == address(0x0) || ei.originalContract == originalContract);
    }

    function getByEffect(address modificatorsContract) view public returns(EffectInfo memory) {
        return effectsInfos[effectToPositionInList[modificatorsContract]];
    }

    function getEffectInfos() view public returns(EffectInfo[] memory) {
        return effectsInfos;
    }
}
